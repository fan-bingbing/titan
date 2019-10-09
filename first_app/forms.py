from django import forms
from first_app.models import RES

class INPUTFREQ(forms.Form):
    test_frequency_in_MHz = forms.FloatField()

class OUTPUTFILE(forms.Form):
    output_filename = forms.CharField()

class INPUTCS(forms.Form):
    filter_choices=[('NA', 'NA'),('NHP-700', 'NHP-700+'),('BHP-300', 'BHP-300')]
    cutoff_choices=[(700, '700MHz'),(300, '300MHz')]
    test_frequency_in_MHz = forms.FloatField()
    cutoff_frequency_in_MHz = forms.ChoiceField(choices=cutoff_choices, widget=forms.Select)
    high_pass_filter = forms.ChoiceField(choices=filter_choices, widget=forms.Select)

class INPUTRES(forms.ModelForm):
    class Meta():
        model = RES
        fields = '__all__'
