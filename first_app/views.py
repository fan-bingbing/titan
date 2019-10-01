from django.shortcuts import render
from first_app.models import FEP, RES, DEMOD, TXSIG, MADOUT
import time
from . import forms
import first_app.definition as df
from first_app.forms import INPUTRES



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

# try:
#     from first_app.forexcel import result
# except BaseException:
#     print("result import failed, it might be damaged")
#     pass


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

    print(res_list[0], res_list[1])

    # form = forms.INPUTRES()
    # if request.method == 'POST': # 'post' will not work here
    #     form = forms.INPUTRES(request.POST)
    #     if form.is_valid():
    #         print("VALIDATION SUCCESS!")
    #         print("equipment available: " + form.cleaned_data['resadd'])
    # return render(request, 'first_app/index.html', {'form':form})# always return input form


    return render(request, 'first_app/index.html', context=res_dict)



def fep(request):
    form = forms.INPUTFREQ()
    if request.method == 'POST': # 'post' will not work here
        form = forms.INPUTFREQ(request.POST)
        if form.is_valid():
            #do something
            print("VALIDATION SUCCESS!")
            print("input frequency: " + str(form.cleaned_data['test_frequency_in_MHz']))
            FSV.FEP_Setup(freq=form.cleaned_data['test_frequency_in_MHz'])
            FSV.query('*OPC?')
            CP50.Set_Freq(freq=form.cleaned_data['test_frequency_in_MHz'])
            CP50.Set_Pow("high")
            CP50.Radio_On()
            time.sleep(2)
            FSV.write("DISP:TRAC:MODE MAXH")
            time.sleep(3)
            FSV.write("DISP:TRAC:MODE VIEW")
            CP50.Radio_Off()
            fep_result = FSV.get_FEP_result(freq=form.cleaned_data['test_frequency_in_MHz'], folder='fep')
            fep_result.update({'form':form})#joint form and result dictionary

            print(f"Frequency error:{fep_result['F']}Hz")
            print(f"Carrier power:{fep_result['P']}dBm")
            # FSV.close()

            return render(request, 'first_app/fep.html', context=fep_result)

    return render(request, 'first_app/fep.html', {'form':form})# always return input form


def mad(request):
    AF_list1 = [100, 300, 500, 700, 900, 1000, 1300, 1500, 1700, 1900, 2000, 2300, 2550] # audio frequency list in Hz
    AF_list2 = [3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 12500]
    Reading_array1 = df.np.zeros(shape=(13,3)) # empty numpy array for below 3kHz result storage
    Reading_array2 = df.np.zeros(shape=(11,3)) # empty numpy array for above 3kHz result storage
    # RSheet = Get_result_sheet("Test_Result.xlsx", "Max_Dev")
    MADOUT.objects.all().delete()

    form = forms.INPUTFREQ()
    if request.method == 'POST': # 'post' will not work here
        form = forms.INPUTFREQ(request.POST)
        if form.is_valid():
            #do something
            print("VALIDATION SUCCESS!")
            print("input frequency: " + str(form.cleaned_data['test_frequency_in_MHz']))
            SMB.Tx_Setup()
            SMB.query('*OPC?')
            FSV.DeMod_Setup(freq=form.cleaned_data['test_frequency_in_MHz'])
            FSV.query('*OPC?')
            CP50.Set_Freq(freq=form.cleaned_data['test_frequency_in_MHz'])
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
                mad_list = MADOUT.objects.get_or_create(audiofreq=AF_list1[i],
                                            audiolev=Level_AF,
                                            pluspeak=Reading_array1[i][0],
                                            minuspeak=Reading_array1[i][1],
                                            avepeak=Reading_array1[i][2],
                                            limit=2.5,
                                            margin=round(2.5-abs(Reading_array1[i][2]),5),
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
                mad_list = MADOUT.objects.get_or_create(audiofreq=AF_list2[i],
                                            audiolev=Level_AF,
                                            pluspeak=Reading_array2[i][0],
                                            minuspeak=Reading_array2[i][1],
                                            avepeak=Reading_array2[i][2],
                                            limit=2.5,
                                            margin=round(2.5-abs(Reading_array2[i][2]),5),
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
