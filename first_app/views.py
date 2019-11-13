from django.shortcuts import render
from first_app.models import FEP, RES, DEMOD, TXSIG, ACPOUT, MADOUT, SENOUT
from first_app.models import FEPOUT, CSEOUT, CSHOUT, BLKOUT, SROUT, ACSOUT
import time, math
from . import forms
import first_app.definition as df
from first_app.forms import INPUTRES
import csv
from django.http import HttpResponse

# equip_list = RES.objects.all()
# FSVIP = equip_list[0].resadd
# SMB1IP = equip_list[1].resadd
# SMB2IP = equip_list[2].resadd
#
# try:
#     FSV = df.SpecAn(FSVIP)
# except BaseException:
#     print("FSV is not on.")
#     pass
#
# try:
#     SMB1 = df.SigGen(SMB1IP)
# except BaseException:
#     print("SMB1 is not on.")
#     pass
#
# try:
#     SMB2 = df.SigGen(SMB2IP)
# except BaseException:
#     print("SMB2 is not on.")
#     pass
#
# try:
#     EUT = df.Radio('com10', baudrate=9600)
# except BaseException:
#     print("Specified com port does not exsit.")
#     pass



try:
    from first_app.definition import FSV
except BaseException:
    print("FSV import failed, FSV might be not on")
    pass

try:
    from first_app.definition import SMB1
except BaseException:
    print("SMB1 import failed, SMB1 might be not on")
    pass

try:
    from first_app.definition import SMB2
except BaseException:
    print("SMB2 import failed, SMB2 might be not on")
    pass

try:
    from first_app.definition import EUT
except BaseException:
    print("EUT import failed, EUT might be not connected.")
    pass

try:
    from first_app.definition import SC
except BaseException:
    print("SC import failed, SC might be not connected.")
    pass


# Create your views here.
def index(request):
    form = forms.INPUTINDEX()
    if request.method == 'POST': # 'post' will not work here
        form = forms.INPUTINDEX(request.POST)
        # if form.is_valid():
            # global FSVIP, SMB1IP, SMB2IP
            # FSVIP = form.cleaned_data['fsv']
            # SMB1IP = form.cleaned_data['smb1']
            # SMB2IP = form.cleaned_data['smb2']

            #do something
            # try:
            #     FSV = SpecAn(form.cleaned_data['fsv'])
            # except BaseException:
            #     print("FSV is NOT not on.")
            #     pass

            # try:
            #     SMB1.close()
            #     # SMB1 = SigGen(form.cleaned_data['smb1'])
            # except BaseException:
            #     print("SMB1 is not on.")
            #     pass
            #
            # try:
            #     SMB2.close()
            #     # SMB2 = SigGen(form.cleaned_data['smb2'])
            # except BaseException:
            #     print("SMB2 is not on.")
            #     pass


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
    res_dict.update({'form':form})

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

            feplist = FEPOUT.objects.all()
            writer.writerow(FEPOUT.objects.filter(Test_name='FEP_test1').values().get())
            for item in feplist:
                writer.writerow(FEPOUT.objects.filter(Test_name=item).values_list().get())
            writer.writerow([''])

            acplist = ACPOUT.objects.all()
            writer.writerow(ACPOUT.objects.filter(Test_name='ACP_test1').values().get())
            for item in acplist:
                writer.writerow(ACPOUT.objects.filter(Test_name=item).values_list().get())
            writer.writerow([''])

            acslist = ACSOUT.objects.all()
            writer.writerow(ACSOUT.objects.filter(Test_name='ACS_test1.1').values().get())
            for item in acslist:
                writer.writerow(ACSOUT.objects.filter(Test_name=item).values_list().get())
            writer.writerow([''])

            srlist = SROUT.objects.all()
            writer.writerow(SROUT.objects.filter(Test_name='SR_test1').values().get())
            for item in srlist:
                writer.writerow(SROUT.objects.filter(Test_name=item).values_list().get())
            writer.writerow([''])

            blklist = BLKOUT.objects.all()
            writer.writerow(BLKOUT.objects.filter(Test_name='BLK_test1.1').values().get())
            for item in blklist:
                writer.writerow(BLKOUT.objects.filter(Test_name=item).values_list().get())
            writer.writerow([''])

            cselist = CSEOUT.objects.all()
            writer.writerow(CSEOUT.objects.filter(Test_name='CSE_test1.1').values().get())
            for item in cselist:
                writer.writerow(CSEOUT.objects.filter(Test_name=item).values_list().get())
            cshlist = CSHOUT.objects.all()
            for item in cshlist:
                writer.writerow(CSHOUT.objects.filter(Test_name=item).values_list().get())
            writer.writerow([''])

            madlist = MADOUT.objects.all()
            writer.writerow(MADOUT.objects.filter(Test_name='MAD_test1.1').values().get())
            for item in madlist:
                writer.writerow(MADOUT.objects.filter(Test_name=item).values_list().get())
            writer.writerow([''])

            return response

    return render(request, 'first_app/output.html', {'form':form})

def cs(request):
    form = forms.INPUTCS()
    if request.method == 'POST': # 'post' will not work here
        form = forms.INPUTCS(request.POST)
        if form.is_valid():
            CSEOUT.objects.all().delete()
            #do something
            print("VALIDATION SUCCESS!")
            test_freq_string = form.cleaned_data['test_frequency_in_MHz']
            cutoff_freq = form.cleaned_data['cutoff_frequency_in_MHz']

            test_freq_list = df.re.findall(r'-?\d+\.\d+', test_freq_string)

            for i, test_freq in enumerate(test_freq_list):# python way of counting in for loop
                test_freq = float(test_freq)
                df.CSE_operation(freq=test_freq, sub_range=1, limit_line=1,
                                 cutoff=cutoff_freq, test_num='CSE_test'+str(i+1)+'.1')
                df.CSE_operation(freq=test_freq, sub_range=2, limit_line=1,
                                 cutoff=cutoff_freq, test_num='CSE_test'+str(i+1)+'.2')
                df.CSE_operation(freq=test_freq, sub_range=3, limit_line=1,
                                 cutoff=cutoff_freq, test_num='CSE_test'+str(i+1)+'.3')


            csl_list = CSEOUT.objects.all()
            csl_dict = {
                    'cslouts': csl_list
                }

            csl_dict.update({'form':form})#joint form and result dictionary

            return render(request, 'first_app/cs.html', context=csl_dict)

    return render(request, 'first_app/cs.html', {'form':form})# always return input form

def csh(request):
    form = forms.INPUTCS()
    if request.method == 'POST': # 'post' will not work here
        form = forms.INPUTCS(request.POST)
        if form.is_valid():
            CSHOUT.objects.all().delete()
            #do something
            print("VALIDATION SUCCESS!")
            test_freq_string = form.cleaned_data['test_frequency_in_MHz']
            cutoff_freq = form.cleaned_data['cutoff_frequency_in_MHz']
            filter = form.cleaned_data['high_pass_filter']

            test_freq_list = df.re.findall(r'-?\d+\.\d+', test_freq_string)

            for i, test_freq in enumerate(test_freq_list):# python way of counting in for loop
                test_freq = float(test_freq)
                df.CSE_operation(freq=test_freq, sub_range=4, limit_line=1, cutoff=cutoff_freq,
                                 filter=filter, test_num='CSE_test'+str(i+1)+'.4')
                df.CSE_operation(freq=test_freq, sub_range=5, limit_line=1, cutoff=cutoff_freq,
                                 filter=filter, test_num='CSE_test'+str(i+1)+'.5')


            csh_list = CSHOUT.objects.all()
            csh_dict = {
                    'cshouts': csh_list
                }

            csh_dict.update({'form':form})#joint form and result dictionary

            return render(request, 'first_app/csh.html', context=csh_dict)

    return render(request, 'first_app/csh.html', {'form':form})# always return input form


def fep(request):
    form = forms.INPUTFEP()
    if request.method == 'POST': # 'post' will not work here
        form = forms.INPUTFEP(request.POST)
        if form.is_valid():
            #do something
            FEPOUT.objects.all().delete()
            print("VALIDATION SUCCESS!")
            test_freq_string = form.cleaned_data['test_frequency_in_MHz']
            test_power = form.cleaned_data['test_power_in_Watt']

            test_freq_list = df.re.findall(r'-?\d+\.\d+', test_freq_string)

            for i, test_freq in enumerate(test_freq_list):# python way of counting in for loop
                test_freq = float(test_freq)
                FSV.FEP_Setup(freq=test_freq)
                FSV.query('*OPC?')
                EUT.Set_Freq(freq=test_freq+0.0125)
                # adding 0.0125MHz makes absolutely no sense but fixed problem...
                EUT.Set_Pow("high")
                EUT.Radio_On()
                time.sleep(2)
                FSV.write("DISP:TRAC:MODE MAXH")
                time.sleep(3)
                FSV.write("DISP:TRAC:MODE VIEW")
                EUT.Radio_Off()

                fep_result = FSV.get_FEP_result(freq=test_freq, folder='fep')
                Timestamp ='{:%d-%b-%Y %H:%M:%S}'.format(df.datetime.datetime.now())
                FEPOUT.objects.get_or_create(Test_name='FEP_test'+str(i+1),
                                            CH_Freq_MHz=test_freq,
                                            Freq_Error_Hz=round(fep_result['F'],5),
                                            Fre_error_limit_Hz=fep_result['F_limit'],
                                            Power_diff_dB=round(abs(fep_result['P']-10*math.log10(test_power*1000)),5),
                                            Power_diff_limit_dB=fep_result['P_limit'],
                                            Screenshot_file='FEP_'+str(test_freq)+'_MHz.png',
                                            TimeStamp=Timestamp
                                            )[0]

                print(f"Frequency error:{fep_result['F']}Hz")
                print(f"Carrier power:{fep_result['P']}dBm")
                # FSV.close()


            fep_list = FEPOUT.objects.all()
            fep_dict = {
                    'fepouts': fep_list
                }

            fep_dict.update({'form':form})#joint form and result dictionary
            return render(request, 'first_app/fep.html', context=fep_dict)

    return render(request, 'first_app/fep.html', {'form':form})# always return input form


def acp(request):
    form = forms.INPUTFREQ()
    if request.method == 'POST': # 'post' will not work here
        form = forms.INPUTFREQ(request.POST)
        if form.is_valid():
            ACPOUT.objects.all().delete()
            # do something
            print("VALIDATION SUCCESS!")

            test_freq_string = form.cleaned_data['test_frequency_in_MHz']

            test_freq_list = df.re.findall(r'-?\d+\.\d+', test_freq_string)

            for i, test_freq in enumerate(test_freq_list):# python way of counting in for loop
                test_freq = float(test_freq)
                SMB1.Tx_Setup()
                SMB1.query('*OPC?')
                FSV.DeMod_Setup(freq=test_freq)
                FSV.query('*OPC?')
                EUT.Set_Freq(freq=test_freq+0.0125)
                EUT.Set_Pow("high")
                EUT.Radio_On()
                time.sleep(2)
                FSV.write(f"INIT:CONT OFF")

                df.Tx_set_standard_test_condition()

                FSV.ACP_Setup(freq=test_freq)
                time.sleep(8)
                FSV.write(f"DISP:TRAC:MODE VIEW")
                EUT.Radio_Off()
                SMB1.write("LFO OFF")# turn off audio output at the end of the test
                FSV.screenshot(file_name='ACP_'+str(test_freq)+'_MHz', folder='acp')
                ACP = FSV.query("CALC:MARK:FUNC:POW:RES? ACP")
                ACP_LIST = df.re.findall(r'-?\d+\.\d+', ACP) # -? with or without negative sign, \d+ one or more digit
                Timestamp ='{:%d-%b-%Y %H:%M:%S}'.format(df.datetime.datetime.now())
                acp_list = ACPOUT.objects.get_or_create(Test_name='ACP_test'+str(i+1),
                                                        Frequency_MHz=test_freq,
                                                        CarrierPower_dBm=round(float(ACP_LIST[0]),5),
                                                        ACPminus_dBc=round(float(ACP_LIST[1]),5),
                                                        ACPplus_dBc=round(float(ACP_LIST[2]),5),
                                                        limit_dBm=-16.0,
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
            #do something
            MADOUT.objects.all().delete()
            print("VALIDATION SUCCESS!")

            test_freq_string = form.cleaned_data['test_frequency_in_MHz']

            test_freq_list = df.re.findall(r'-?\d+\.\d+', test_freq_string)
            for i, test_freq in enumerate(test_freq_list):# python way of counting in for loop
                test_freq = float(test_freq)
                SMB1.Tx_Setup()
                SMB1.query('*OPC?')
                FSV.DeMod_Setup(freq=test_freq)
                FSV.query('*OPC?')
                EUT.Set_Freq(freq=test_freq+0.0125)
                EUT.Set_Pow("high")
                EUT.Radio_On()
                time.sleep(2)
                FSV.write(f"INIT:CONT OFF")
                Level_AF = df.Tx_set_standard_test_condition()
                # below code block is to vary audio frequency to complete the test
                Level_AF = 10*Level_AF # bring audio level up 20dB in one step( 10times valtage)
                SMB1.write(f"LFO:VOLT {Level_AF}mV")
                print(f"Audio level has been set to {Level_AF} mV")

                for j in range(0,13):
                    print(f"At Audio frequency:{AF_list1[j]}")
                    SMB1.write(f"LFO:FREQ {AF_list1[j]}Hz")
                    SMB1.query('*OPC?')
                    time.sleep(1)
                    FSV.write(f"INIT:CONT OFF")
                    time.sleep(1)
                    Reading_array1[j][0]= round((float(FSV.query("CALC:MARK:FUNC:ADEM:FM? PPE"))/1000),5)
                    Reading_array1[j][1]= round((float(FSV.query("CALC:MARK:FUNC:ADEM:FM? MPE"))/1000),5)
                    Reading_array1[j][2]= round((float(FSV.query("CALC:MARK:FUNC:ADEM:FM? MIDD"))/1000),5)
                    FSV.query("*OPC?")
                    FSV.write(f"INIT:CONT ON")
                    print(f"Deviation is {Reading_array1[j]}kHz")
                    Timestamp ='{:%d-%b-%Y %H:%M:%S}'.format(df.datetime.datetime.now())
                    mad_list = MADOUT.objects.get_or_create(Test_name='MAD_test'+str(i+1)+'.'+str(j+1),
                                                CH_Freq_MHz=test_freq,
                                                audiofreq_Hz=AF_list1[j],
                                                audiolev_mV=Level_AF,
                                                pluspeak_kHz=Reading_array1[j][0],
                                                minuspeak_kHz=Reading_array1[j][1],
                                                avepeak_kHz=Reading_array1[j][2],
                                                limit_kHz=2.5,
                                                margin_kHz=round(2.5-abs(Reading_array1[j][2]),5),
                                                TimeStamp=Timestamp
                                                )[0]
                Level_AF = Level_AF/10
                SMB1.write(f"LFO:VOLT {Level_AF}mV")
                print(f"Audio level has been set to {Level_AF} mV")

                for j in range(0,11):
                    print(f"At Audio frequency:{AF_list2[j]}")
                    SMB1.write(f"LFO:FREQ {AF_list2[j]}Hz")
                    SMB1.query('*OPC?')
                    time.sleep(1)
                    FSV.write(f"INIT:CONT OFF")
                    time.sleep(1)
                    Reading_array2[j][0]= round(float(FSV.query("CALC:MARK:FUNC:ADEM:FM? PPE"))/1000,5)
                    Reading_array2[j][1]= round(float(FSV.query("CALC:MARK:FUNC:ADEM:FM? MPE"))/1000,5)
                    Reading_array2[j][2]= round(float(FSV.query("CALC:MARK:FUNC:ADEM:FM? MIDD"))/1000,5)
                    FSV.query("*OPC?")
                    FSV.write(f"INIT:CONT ON")
                    print(f"Deviation is {Reading_array2[j]}kHz")
                    Timestamp ='{:%d-%b-%Y %H:%M:%S}'.format(df.datetime.datetime.now())
                    MADOUT.objects.get_or_create(Test_name='MAD_test'+str(i+1)+'.'+str(j+14),
                                                CH_Freq_MHz=test_freq,
                                                audiofreq_Hz=AF_list2[j],
                                                audiolev_mV=Level_AF,
                                                pluspeak_kHz=Reading_array2[j][0],
                                                minuspeak_kHz=Reading_array2[j][1],
                                                avepeak_kHz=Reading_array2[j][2],
                                                limit_kHz=2.5,
                                                margin_kHz=round(2.5-abs(Reading_array2[j][2]),5),
                                                TimeStamp=Timestamp
                                                )[0]
                EUT.Radio_Off()
                SMB1.write("LFO OFF")# turn off audio output at the end of the test
                indication = (FSV.query("*OPC?")).replace("1","Completed.")
                print(f"Maximum Deviation test {indication}")



            mad_list = MADOUT.objects.all()
            mad_dict = {
                    'madouts': mad_list
                }

            mad_dict.update({'form':form})#joint form and result dictionary
            return render(request, 'first_app/mad.html', context=mad_dict)

    return render(request, 'first_app/mad.html', {'form':form})# always return input form

def sen(request):
    form = forms.INPUTFREQ()
    if request.method == 'POST': # 'post' will not work here
        form = forms.INPUTFREQ(request.POST)
        if form.is_valid():
            #do something
            SENOUT.objects.all().delete()
            print("VALIDATION SUCCESS!")

            test_freq_string = form.cleaned_data['test_frequency_in_MHz']
            test_freq_list = df.re.findall(r'-?\d+\.\d+', test_freq_string)
            for i, test_freq in enumerate(test_freq_list):# python way of counting in for loop
                test_freq = float(test_freq)
                SEN = df.Rx_test_operation(freq=test_freq, delta=0.0125, SEN='ON')
                Timestamp ='{:%d-%b-%Y %H:%M:%S}'.format(df.datetime.datetime.now())
                SENOUT.objects.get_or_create(Test_name='SEN_test'+str(i+1),
                                            CH_Freq_MHz=test_freq,
                                            CH_Lev_dBuV=SMB1.Lev_RF(),
                                            Lev_RxPort_dBm=SEN[0],
                                            SINAD_dB=SEN[1],
                                            limit_dB=-120,
                                            TimeStamp=Timestamp
                                            )[0]

            EUT.Radio_Off()
            SMB1.write("OUTP1 OFF")# turn off audio output at the end of the test
            # SMB2.write("OUTP1 OFF")
            print("Sensitivity test completed.")


        sen_list = SENOUT.objects.all()
        sen_dict = {
                'senouts': sen_list
            }

        sen_dict.update({'form':form})#joint form and result dictionary
        return render(request, 'first_app/sen.html', context=sen_dict)
    return render(request, 'first_app/sen.html', {'form':form})# always return input form

def acs(request):

    form = forms.INPUTFREQ()
    if request.method == 'POST': # 'post' will not work here
        form = forms.INPUTFREQ(request.POST)
        if form.is_valid():
            #do something
            ACSOUT.objects.all().delete()
            print("VALIDATION SUCCESS!")

            test_freq_string = form.cleaned_data['test_frequency_in_MHz']
            test_freq_list = df.re.findall(r'-?\d+\.\d+', test_freq_string)
            for i, test_freq in enumerate(test_freq_list):# python way of counting in for loop
                test_freq = float(test_freq)
                ACS_high = df.Rx_test_operation(freq=test_freq, delta=0.0125)
                Timestamp ='{:%d-%b-%Y %H:%M:%S}'.format(df.datetime.datetime.now())
                acs_list = ACSOUT.objects.get_or_create(Test_name='ACS_test'+str(i+1)+'.1',
                                            CH_Freq_MHz=test_freq,
                                            CH_Lev_dBuV=SMB1.Lev_RF(),
                                            IN_Freq_MHz=float(SMB2.Freq_RF())/1e6,
                                            IN_Lev_dBuV=SMB2.Lev_RF(),
                                            ACS_dB=ACS_high,
                                            limit_dB=60.0,
                                            TimeStamp=Timestamp
                                            )[0]

                ACS_low = df.Rx_test_operation(freq=test_freq, delta=-0.0125)
                Timestamp ='{:%d-%b-%Y %H:%M:%S}'.format(df.datetime.datetime.now())
                acs_list = ACSOUT.objects.get_or_create(Test_name='ACS_test'+str(i+1)+'.2',
                                            CH_Freq_MHz=test_freq,
                                            CH_Lev_dBuV=SMB1.Lev_RF(),
                                            IN_Freq_MHz=float(SMB2.Freq_RF())/1e6,
                                            IN_Lev_dBuV=SMB2.Lev_RF(),
                                            ACS_dB=ACS_low,
                                            limit_dB=60.0,
                                            TimeStamp=Timestamp
                                            )[0]
            EUT.Radio_Off()
            SMB1.write("OUTP1 OFF")# turn off audio output at the end of the test
            SMB2.write("OUTP1 OFF")
            print("Adjacent Channel Selectivity test completed.")


        acs_list = ACSOUT.objects.all()
        acs_dict = {
                'acsouts': acs_list
            }

        acs_dict.update({'form':form})#joint form and result dictionary
        return render(request, 'first_app/acs.html', context=acs_dict)
    return render(request, 'first_app/acs.html', {'form':form})# always return input form

def sr(request):

    form = forms.INPUTFREQ()
    if request.method == 'POST': # 'post' will not work here
        form = forms.INPUTFREQ(request.POST)
        if form.is_valid():
            #do something
            SROUT.objects.all().delete()
            print("VALIDATION SUCCESS!")
            test_freq_string = form.cleaned_data['test_frequency_in_MHz']
            test_freq_list = df.re.findall(r'-?\d+\.\d+', test_freq_string)
            for i, test_freq in enumerate(test_freq_list):# python way of counting in for loop
                test_freq = float(test_freq)
                SR = df.Rx_test_operation(freq=test_freq, delta=-2*21.4, step=1.0)
                Timestamp ='{:%d-%b-%Y %H:%M:%S}'.format(df.datetime.datetime.now())
                sr_list = SROUT.objects.get_or_create(Test_name='SR_test'+str(i+1),
                                            CH_Freq_MHz=test_freq,
                                            CH_Lev_dBuV=SMB1.Lev_RF(),
                                            IN_Freq_MHz=float(SMB2.Freq_RF())/1e6,
                                            IN_Lev_dBuV=SMB2.Lev_RF(),
                                            SR_dB=SR,
                                            limit_dB=70.0,
                                            TimeStamp=Timestamp
                                            )[0]

            EUT.Radio_Off()
            SMB1.write("OUTP1 OFF")# turn off audio output at the end of the test
            SMB2.write("OUTP1 OFF")
            print("Spurious Response test completed.")


        sr_list = SROUT.objects.all()
        sr_dict = {
                'srouts': sr_list
            }

        sr_dict.update({'form':form})#joint form and result dictionary
        return render(request, 'first_app/sr.html', context=sr_dict)

    return render(request, 'first_app/sr.html', {'form':form})# always return input form

def blk(request):

    form = forms.INPUTFREQ()
    if request.method == 'POST': # 'post' will not work here
        form = forms.INPUTFREQ(request.POST)
        if form.is_valid():
            #do something
            BLKOUT.objects.all().delete()
            print("VALIDATION SUCCESS!")
            test_freq_string = form.cleaned_data['test_frequency_in_MHz']
            test_freq_list = df.re.findall(r'-?\d+\.\d+', test_freq_string)
            for i, test_freq in enumerate(test_freq_list):# python way of counting in for loop
                test_freq = float(test_freq)
                BLK_high = df.Rx_test_operation(freq=test_freq, delta=1.0, UMD='OFF', step=1.0)
                Timestamp ='{:%d-%b-%Y %H:%M:%S}'.format(df.datetime.datetime.now())
                blk_list = BLKOUT.objects.get_or_create(Test_name='BLK_test'+str(i+1)+'.1',
                                            CH_Freq_MHz=test_freq,
                                            CH_Lev_dBuV=SMB1.Lev_RF(),
                                            IN_Freq_MHz=float(SMB2.Freq_RF())/1e6,
                                            IN_Lev_dBuV=SMB2.Lev_RF(),
                                            BLK_dB=BLK_high,
                                            limit_dB=80.0,
                                            TimeStamp=Timestamp
                                            )[0]

                BLK_low = df.Rx_test_operation(freq=test_freq, delta=-1.0, UMD='OFF', step=1.0)
                Timestamp ='{:%d-%b-%Y %H:%M:%S}'.format(df.datetime.datetime.now())
                blk_list = BLKOUT.objects.get_or_create(Test_name='BLK_test'+str(i+1)+'.2',
                                            CH_Freq_MHz=test_freq,
                                            CH_Lev_dBuV=SMB1.Lev_RF(),
                                            IN_Freq_MHz=float(SMB2.Freq_RF())/1e6,
                                            IN_Lev_dBuV=SMB2.Lev_RF(),
                                            BLK_dB=BLK_low,
                                            limit_dB=80.0,
                                            TimeStamp=Timestamp
                                            )[0]
            EUT.Radio_Off()
            SMB1.write("OUTP1 OFF")# turn off audio output at the end of the test
            SMB2.write("OUTP1 OFF")
            print("Blocking test completed.")


        blk_list = BLKOUT.objects.all()
        blk_dict = {
                'blkouts': blk_list
            }

        blk_dict.update({'form':form})#joint form and result dictionary
        return render(request, 'first_app/blk.html', context=blk_dict)

    return render(request, 'first_app/blk.html', {'form':form})# always return input form
