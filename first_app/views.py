from django.shortcuts import render
from first_app.models import FEP, RES
import time
from . import forms
import first_app.definition as df

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


# Create your views here.
def index(request):
    # if request.method == 'POST': # 'post' will not work here
    #     print("SEARCH SUCCESS!")
    rm = df.pyvisa.ResourceManager()
    print(rm.list_resources())

    for item in rm.list_resources():
        try:
            inst = rm.open_resource(item)
            id = inst.query("*IDN?")
            print(id)
            res_list = RES.objects.get_or_create(resadd=item, resid=id)[0]

        except BaseException:
            print("device is not talkable.")
        pass

    res_list = RES.objects.order_by('resid')
    res_dict = {
        'equips': res_list
    }

    return render(request, 'first_app/index.html', context=res_dict)

def fep(request):
    form = forms.INPUTFREQ()
    if request.method == 'POST': # 'post' will not work here
        form = forms.INPUTFREQ(request.POST)
        if form.is_valid():
            #do something
            print("VALIDATION SUCCESS!")
            print("input frequency: " + form.cleaned_data['test_frequency_in_MHz'])
            FSV.FEP_Setup(freq=float(form.cleaned_data['test_frequency_in_MHz']))
            FSV.query('*OPC?')
            CP50.Set_Freq(freq=float(form.cleaned_data['test_frequency_in_MHz']))
            CP50.Set_Pow("high")
            CP50.Radio_On()
            time.sleep(2)
            FSV.write("DISP:TRAC:MODE MAXH")
            time.sleep(3)
            FSV.write("DISP:TRAC:MODE VIEW")
            CP50.Radio_Off()
            fep_result = FSV.get_FEP_result(freq=float(form.cleaned_data['test_frequency_in_MHz']))
            fep_result.update({'form':form})#joint form and result dictionary
            print(f"Frequency error:{fep_result['F']}Hz")
            print(f"Carrier power:{fep_result['P']}dBm")
            # FSV.close()
            return render(request, 'first_app/fep.html', context=fep_result)

    return render(request, 'first_app/fep.html', {'form':form})# always return input form
