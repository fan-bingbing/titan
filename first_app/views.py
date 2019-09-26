from django.shortcuts import render
from first_app.models import FEP
import time
from . import forms


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
    return render(request, 'first_app/index.html')

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
            fep_result.update({'form':form})
            print(f"Frequency error:{fep_result['F']}Hz")
            print(f"Carrier power:{fep_result['P']}dBm")
            # FSV.close()
            return render(request, 'first_app/fep.html', context=fep_result)

    # return render(request, 'first_app/fep.html', {'form':form})
