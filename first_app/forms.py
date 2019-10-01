from django import forms
from first_app.models import RES

class INPUTFREQ(forms.Form):
    test_frequency_in_MHz = forms.FloatField()



class INPUTRES(forms.ModelForm):
    class Meta():
        model = RES
        fields = '__all__'
