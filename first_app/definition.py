import pyvisa
import sys
import os
import math
# import openpyxl
# import pandas as pd
# from openpyxl import Workbook
# from openpyxl import load_workbook

import serial
import re
# import config
import datetime
from decimal import * # should aviod wildcard import mentioned in PEP08
getcontext().prec = 10 # set 10 decimal values precision
# Decimal module import from decimal make sure float numbers addition yeilds correct value
# import sounddevice as sd
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.fftpack import fft
# import subprocess
# from os import system
# from subprocess import Popen, PIPE
from first_app.models import FEP


class SpecAn(object):
    def __init__(self, address):
        self.rm = pyvisa.ResourceManager()
        self.SP = self.rm.open_resource(address) # Spec An

    def write(self, str):
        self.SP.write(str)

    def query(self, str):
        return self.SP.query(str)

    def close(self):
        self.SP.close()

    def screenshot(self, file_name):
        self.SP.write("HCOP:DEV:LANG PNG") # set file type to .png
        self.SP.write("HCOP:CMAP:DEF4")
        self.SP.write(f"MMEM:NAME \'c:\\temp\\Dev_Screenshot.png\'")
        self.SP.write("HCOP:IMM") # perform copy and save .png file on SpecAn
        self.SP.query("*OPC?")

        file_data = self.SP.query_binary_values(f"MMEM:DATA? \'c:\\temp\\Dev_Screenshot.png\'", datatype='s',)[0] # query binary data and save
        # new_file = open(f"c:\\Temp\\{file_name}.png", "wb")
        new_file = open(f"c:\\Users\\afan\\Documents\\titan\\static\\result_images\\{file_name}.png", "wb")# open a new file as "binary/write" on PC
        new_file.write(file_data) # copy data to the file on PC
        new_file.close()
        print(f"Screenshot saved to PC c:\\Users\\afan\\Documents\\titan\\static\\result_images\\{file_name}.png\n")

    def FEP_Setup(self, freq):
        fep_list = FEP.objects.all()
        self.SP.write(f"*RST") # write all paramaters to SpecAn
        self.SP.write("SYST:DISP:UPD ON")
        self.SP.write(f"FREQ:CENT {freq}MHz")
        self.SP.write(f"FREQ:SPAN {fep_list[1].content}Hz")
        self.SP.write(f"BAND {fep_list[2].content}Hz")
        self.SP.write(f"BAND:VID {fep_list[3].content}Hz")
        self.SP.write(f"DISP:TRAC:Y:RLEV:OFFS {fep_list[6].content}")
        self.SP.write(f"DISP:TRAC:Y:RLEV {fep_list[4].content}")
        self.SP.write(f"INP:ATT {fep_list[5].content}")
        self.SP.write(f"{fep_list[7].content}")
        self.SP.write(f"CORR:TRAN:SEL '{fep_list[8].content}'")
        self.SP.write(f"CORR:TRAN {fep_list[9].content} ")
        self.SP.write(f"CORR:TRAN:SEL '{fep_list[10].content}'")
        self.SP.write(f"CORR:TRAN {fep_list[11].content}")
        self.SP.write(f"CORR:TRAN:SEL '{fep_list[12].content}'")
        self.SP.write(f"CORR:TRAN {fep_list[13].content}")
        self.SP.write(f"CALC:LIM:NAME '{fep_list[14].content}'")
        self.SP.write(f"CALC:LIM:UPP:STAT {fep_list[15].content}")
        self.SP.write(f"CALC:LIM:NAME '{fep_list[16].content}'")
        self.SP.write(f"CALC:LIM:UPP:STAT {fep_list[17].content}")
        self.SP.write(f"SWE:POIN {fep_list[18].content}")

    def get_FEP_result(self, freq):
        self.SP.write("CALC:MARK1:MAX")
        Frequency = self.SP.query("CALC:MARK1:X?")
        Level = float(self.SP.query("CALC:MARK1:Y?"))
        Frequency_error = float(Frequency) - float(self.SP.query("FREQ:CENT?"))
        indication = (self.SP.query("*OPC?")).replace("1","Completed.")
        self.screenshot('FEP_'+str(freq)+'MHz')
        return {'F':Frequency_error, 'F_limit':1500, 'F_margin':1500 - abs(Frequency_error),
                'P':Level, 'P_limit':36.98, 'P_margin':abs(Level - 36.98),
                }


class Radio(object):
    def __init__(self, com):
        self.ESC_CHAR = 0x7D # Escape char
        self.STX_CHAR =  0x7E # Start of packet
        self.ETX_CHAR = 0x7F # End of packet
        self.CHECKSUM_XOR_MASK = 0xFF

        self.payload0 = bytearray(b'\xB4\x88\x2a\x80')# set carrie freq 136MHz basd on 12.5kHz calculation
        self.payload1 = bytearray(b'\xB4\x93\x03')# set 25W power
        self.payload2 = bytearray(b'\xA6\x01') # PTT ON
        self.payload3 = bytearray(b'\xB4\x91\x03\xE8')# 1kHz audio on
        self.payload4 = bytearray(b'\xB4\x91\x0B\xB8')# 3kHz audio on
        self.payload5 = bytearray(b'\xB4\x91\x00\x00')# audio off
        self.payload6 = bytearray(b'\xB4\x82\x10')# selcall tone on
        self.payload7 = bytearray(b'\xB4\x82\x0f')# selcall tone off
        self.payload8 = bytearray(b'\xA6\x00') # PTT off

        self.port = com
        self.baudrate = 115200
        self.timeout = None
        self.ser = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)  # open serial port

    def Packet_Gen(self, payload): # return GME2 protocol packet
        # Header
        tx_array = bytearray((self.STX_CHAR, 2, len(payload)))

        # Escape the payload, append it to the output buffer, make the checksum
        chksum = 0
        for i, b in enumerate(payload):
            # The first word of the payload is always the command ID.
            # The MSB of the command ID is always 1. The radio just
            # clears it in the ACK, without doing anything else with it.
            if i == 0:
                bb = (0x80 | b) & 0xFF
            else:
                bb = b & 0xFF
            chksum ^= bb
            if bb in (self.ESC_CHAR, self.STX_CHAR, self.ETX_CHAR):
                tx_array.append(self.ESC_CHAR)
                tx_array.append(bb ^ 0x20)
            else:
                tx_array.append(bb)

        # Trailer
        tx_array.append(chksum ^ self.CHECKSUM_XOR_MASK)
        tx_array.append(self.ETX_CHAR)

        return tx_array

    def Set_Freq(self, freq):
        a = ((hex(int((Decimal(freq)*Decimal(1e6))/(Decimal(12.5*1e3))))[2]+hex(int((Decimal(freq)*Decimal(1e6))/Decimal((12.5*1e3))))[3]))# calculate first HEX of input frequency
        b = ((hex(int((Decimal(freq)*Decimal(1e6))/(Decimal(12.5*1e3))))[4]+hex(int((Decimal(freq)*Decimal(1e6))/Decimal((12.5*1e3))))[5]))# calculate second HEX of input frequency
        self.payload0[2] = int(a,16) # assign first DEC (transferred from HEX) to the third number of paylaod0
        self.payload0[3] = int(b,16) # assign second DEC (transferred from HEX) to the fourth number of paylaod0
        self.ser.write(self.Packet_Gen(self.payload0))
        print(f"radio frequency has been set to {freq} MHz.")

    def Set_Pow(self, pow):
        if pow == "low":
            self.payload1[2] = 0
        elif pow == "high":
            self.payload1[2] = 3
        else:
            print("Set_Pow() only accept 'low' or 'high'")
        print(f"radio power has been set to {pow}.")

        self.ser.write(self.Packet_Gen(self.payload1))

    def Radio_On(self):
        self.ser.write(self.Packet_Gen(self.payload2))
        print("Radio's on")

    def Radio_Off(self):
        self.ser.write(self.Packet_Gen(self.payload8))
        print("Radio's off")

    def Radio_close(self):
        self.ser.close()
        print("Serial session is closed.")

try:
    FSV = SpecAn('TCPIP0::10.0.22.28::inst0::INSTR')
except BaseException:
    print("FSV is not on.")
    pass

try:
    CP50 = Radio('com7')
except BaseException:
    print("Specified com port does not exsit.")
    pass
