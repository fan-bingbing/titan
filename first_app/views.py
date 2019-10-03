from django.shortcuts import render
from first_app.models import FEP, RES, DEMOD, TXSIG, ACPOUT, MADOUT, CSEOUT
import time
from . import forms
import first_app.definition as df
from first_app.forms import INPUTRES
import csv
from django.http import HttpResponse

try:
    from first_app.definition import FSV
except BaseException:
    print("FSV import failed, FSV might be not on")
    pass

try:
    from first_app.definition import CP50
except BaseException:
    print("CP50 import failed, CP50 might be not connected.")
    pass

try:
    from first_app.definition import SMB
except BaseException:
    print("SMB import failed, SMB might be not on")
    pass


# Create your views here.
def index(request):
    # if request.method == 'POST': # 'post' will not work here
    #     print("SEARCH SUCCESS!")
    rm = df.pyvisa.ResourceManager()
    print(rm.list_resources())
    RES.objects.all().delete()# delete all objects(entries) at start
    for item in rm.list_resources():
        try:
            inst = rm.open_resource(item)
            id = inst.query("*IDN?")
            print(id)
            res_list = RES.objects.get_or_create(resadd=item, resid=id)[0]

        except BaseException:
            print("device is not talkable.")
        pass

    res_list = RES.objects.all()
    res_dict = {
        'equips': res_list
    }

    return render(request, 'first_app/index.html', context=res_dict)

def output(request):
    form = forms.OUTPUTFILE()
    if request.method == 'POST': # 'post' will not work here
        form = forms.OUTPUTFILE(request.POST)
        if form.is_valid():
            #do something
            filename = form.cleaned_data['output_filename'] + '.csv'
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename={filename}'

            writer = csv.writer(response)

            AF_list = MADOUT.objects.all() # get a audio freq list from MADOUT

            # write MADOUT fields in first row
            writer.writerow(MADOUT.objects.filter(audiofreq_Hz=100).values().get())
            # write whole table
            for item in AF_list:
                writer.writerow(MADOUT.objects.filter(audiofreq_Hz=item).values_list().get())

            return response

    return render(request, 'first_app/output.html', {'form':form})

def cs(request):
    form = forms.INPUTFREQ()
    if request.method == 'POST': # 'post' will not work here
        form = forms.INPUTFREQ(request.POST)
        if form.is_valid():
            CSEOUT.objects.all().delete()
            #do something
            print("VALIDATION SUCCESS!")
            test_freq = form.cleaned_data['test_frequency_in_MHz']
            print("input frequency: " + str(test_freq))
            df.CSE_operation(freq=test_freq, sub_range=1, limit_line=1)
            df.CSE_operation(freq=test_freq, sub_range=2, limit_line=1)
            df.CSE_operation(freq=test_freq, sub_range=3, limit_line=1)
            cse_list = CSEOUT.objects.all()
            cse_dict = {
                    'cseouts': cse_list
                }

            cse_dict.update({'form':form})#joint form and result dictionary

            return render(request, 'first_app/cs.html', context=cse_dict)

    return render(request, 'first_app/cs.html', {'form':form})# always return input form


def fep(request):
    form = forms.INPUTFREQ()
    if request.method == 'POST': # 'post' will not work here
        form = forms.INPUTFREQ(request.POST)
        if form.is_valid():
            #do something
            print("VALIDATION SUCCESS!")
            test_freq = form.cleaned_data['test_frequency_in_MHz']
            print("input frequency: " + str(test_freq))
            FSV.FEP_Setup(freq=test_freq)
            FSV.query('*OPC?')
            CP50.Set_Freq(freq=test_freq)
            CP50.Set_Pow("high")
            CP50.Radio_On()
            time.sleep(2)
            FSV.write("DISP:TRAC:MODE MAXH")
            time.sleep(3)
            FSV.write("DISP:TRAC:MODE VIEW")
            CP50.Radio_Off()
            fep_result = FSV.get_FEP_result(freq=test_freq, folder='fep')
            fep_result.update({'form':form})#joint form and result dictionary

            print(f"Frequency error:{fep_result['F']}Hz")
            print(f"Carrier power:{fep_result['P']}dBm")
            # FSV.close()

            return render(request, 'first_app/fep.html', context=fep_result)

    return render(request, 'first_app/fep.html', {'form':form})# always return input form


def acp(request):
    form = forms.INPUTFREQ()
    if request.method == 'POST': # 'post' will not work here
        form = forms.INPUTFREQ(request.POST)
        if form.is_valid():
            ACPOUT.objects.all().delete()
            # do something
            print("VALIDATION SUCCESS!")
            test_freq = form.cleaned_data['test_frequency_in_MHz']
            print("input frequency: " + str(test_freq))
            SMB.Tx_Setup()
            SMB.query('*OPC?')
            FSV.DeMod_Setup(freq=test_freq)
            FSV.query('*OPC?')
            CP50.Set_Freq(freq=test_freq)
            CP50.Set_Pow("high")
            CP50.Radio_On()
            time.sleep(2)
            FSV.write(f"INIT:CONT OFF")

            df.Tx_set_standard_test_condition()

            FSV.ACP_Setup(freq=test_freq)
            time.sleep(8)
            FSV.write(f"DISP:TRAC:MODE VIEW")
            CP50.Radio_Off()
            SMB.write("LFO OFF")# turn off audio output at the end of the test
            FSV.screenshot(file_name='ACP_'+str(test_freq)+'_MHz', folder='acp')
            ACP = FSV.query("CALC:MARK:FUNC:POW:RES? ACP")
            ACP_LIST = df.re.findall(r'-?\d+\.\d+', ACP) # -? with or without negative sign, \d+ one or more digit
            Timestamp ='{:%d-%b-%Y %H:%M:%S}'.format(df.datetime.datetime.now())
            acp_list = ACPOUT.objects.get_or_create(Frequency_MHz=test_freq,
                                                    CarrierPower_dBm=round(float(ACP_LIST[0]),5),
                                                    ACPminus_dBc=round(float(ACP_LIST[1]),5),
                                                    ACPplus_dBc=round(float(ACP_LIST[2]),5),
                                                    Screenshot_file='ACP_'+str(test_freq)+'_MHz.png',
                                                    TimeStamp=Timestamp,
                                                    )[0]
            indication = (FSV.query("*OPC?")).replace("1","Completed.")
            print(f"Adjacent Channel Test {indication}")
            print(ACP_LIST)
            acp_list = ACPOUT.objects.all()
            acp_dict = {
                    'acpouts': acp_list
                }

            acp_dict.update({'form':form})#joint form and result dictionary
            return render(request, 'first_app/acp.html', context=acp_dict)

    return render(request, 'first_app/acp.html', {'form':form})# always return input form



def mad(request):
    AF_list1 = [100, 300, 500, 700, 900, 1000, 1300, 1500, 1700, 1900, 2000, 2300, 2550] # audio frequency list in Hz
    AF_list2 = [3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 12500]
    Reading_array1 = df.np.zeros(shape=(13,3)) # empty numpy array for below 3kHz result storage
    Reading_array2 = df.np.zeros(shape=(11,3)) # empty numpy array for above 3kHz result storage
    # RSheet = Get_result_sheet("Test_Result.xlsx", "Max_Dev")

    form = forms.INPUTFREQ()
    if request.method == 'POST': # 'post' will not work here
        form = forms.INPUTFREQ(request.POST)
        if form.is_valid():
            MADOUT.objects.all().delete()
            #do something
            print("VALIDATION SUCCESS!")
            test_freq = form.cleaned_data['test_frequency_in_MHz']
            print("input frequency: " + str(test_freq))
            SMB.Tx_Setup()
            SMB.query('*OPC?')
            FSV.DeMod_Setup(freq=test_freq)
            FSV.query('*OPC?')
            CP50.Set_Freq(freq=test_freq)
            CP50.Set_Pow("high")
            CP50.Radio_On()
            time.sleep(2)
            FSV.write(f"INIT:CONT OFF")
            Level_AF = df.Tx_set_standard_test_condition()
            # below code block is to vary audio frequency to complete the test
            Level_AF = 10*Level_AF # bring audio level up 20dB in one step( 10times valtage)
            SMB.write(f"LFO:VOLT {Level_AF}mV")
            print(f"Audio level has been set to {Level_AF} mV")

            for i in range(0,13):
                print(f"At Audio frequency:{AF_list1[i]}")
                SMB.write(f"LFO:FREQ {AF_list1[i]}Hz")
                SMB.query('*OPC?')
                time.sleep(1)
                FSV.write(f"INIT:CONT OFF")
                time.sleep(1)
                Reading_array1[i][0]= round((float(FSV.query("CALC:MARK:FUNC:ADEM:FM? PPE"))/1000),5)
                Reading_array1[i][1]= round((float(FSV.query("CALC:MARK:FUNC:ADEM:FM? MPE"))/1000),5)
                Reading_array1[i][2]= round((float(FSV.query("CALC:MARK:FUNC:ADEM:FM? MIDD"))/1000),5)
                FSV.query("*OPC?")
                FSV.write(f"INIT:CONT ON")
                print(f"Deviation is {Reading_array1[i]}kHz")
                Timestamp ='{:%d-%b-%Y %H:%M:%S}'.format(df.datetime.datetime.now())
                mad_list = MADOUT.objects.get_or_create(audiofreq_Hz=AF_list1[i],
                                            audiolev_mV=Level_AF,
                                            pluspeak_kHz=Reading_array1[i][0],
                                            minuspeak_kHz=Reading_array1[i][1],
                                            avepeak_kHz=Reading_array1[i][2],
                                            limit_kHz=2.5,
                                            margin_kHz=round(2.5-abs(Reading_array1[i][2]),5),
                                            timestamp=Timestamp
                                            )[0]
            Level_AF = Level_AF/10
            SMB.write(f"LFO:VOLT {Level_AF}mV")
            print(f"Audio level has been set to {Level_AF} mV")

            for i in range(0,11):
                print(f"At Audio frequency:{AF_list2[i]}")
                SMB.write(f"LFO:FREQ {AF_list2[i]}Hz")
                SMB.query('*OPC?')
                time.sleep(1)
                FSV.write(f"INIT:CONT OFF")
                time.sleep(1)
                Reading_array2[i][0]= round(float(FSV.query("CALC:MARK:FUNC:ADEM:FM? PPE"))/1000,5)
                Reading_array2[i][1]= round(float(FSV.query("CALC:MARK:FUNC:ADEM:FM? MPE"))/1000,5)
                Reading_array2[i][2]= round(float(FSV.query("CALC:MARK:FUNC:ADEM:FM? MIDD"))/1000,5)
                FSV.query("*OPC?")
                FSV.write(f"INIT:CONT ON")
                print(f"Deviation is {Reading_array2[i]}kHz")
                Timestamp ='{:%d-%b-%Y %H:%M:%S}'.format(df.datetime.datetime.now())
                mad_list = MADOUT.objects.get_or_create(audiofreq_Hz=AF_list2[i],
                                            audiolev_mV=Level_AF,
                                            pluspeak_kHz=Reading_array2[i][0],
                                            minuspeak_kHz=Reading_array2[i][1],
                                            avepeak_kHz=Reading_array2[i][2],
                                            limit_kHz=2.5,
                                            margin_kHz=round(2.5-abs(Reading_array2[i][2]),5),
                                            timestamp=Timestamp
                                            )[0]
            CP50.Radio_Off()
            SMB.write("LFO OFF")# turn off audio output at the end of the test
            indication = (FSV.query("*OPC?")).replace("1","Completed.")
            print(f"Maximum Deviation test {indication}")
            mad_list = MADOUT.objects.all()
            mad_dict = {
                    'madouts': mad_list
                }

            mad_dict.update({'form':form})#joint form and result dictionary
            return render(request, 'first_app/mad.html', context=mad_dict)

    return render(request, 'first_app/mad.html', {'form':form})# always return input form
