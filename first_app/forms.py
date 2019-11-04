from django import forms
from first_app.models import RES
equip_list = RES.objects.all()

class INPUTFEP(forms.Form):
    test_frequency_in_MHz = forms.FloatField()
    test_power_in_Watt = forms.FloatField()




class OUTPUTFILE(forms.Form):
    output_filename = forms.CharField()

class INPUTINDEX(forms.Form):
    fsv_choices=[(x, y) for x in equip_list for y in equip_list if x == y]
    smb1_choices=[(x, y) for x in equip_list for y in equip_list if x == y]
    smb2_choices=[(x, y) for x in equip_list for y in equip_list if x == y]
    fsv = forms.ChoiceField(choices=fsv_choices, widget=forms.Select)
    smb1 = forms.ChoiceField(choices=smb1_choices, widget=forms.Select)
    smb2 = forms.ChoiceField(choices=smb2_choices, widget=forms.Select)

class INPUTCS(forms.Form):
    filter_choices=[('NA', 'NA'),('NHP-700', 'NHP-700+'),('BHP-300', 'BHP-300')]
    cutoff_choices=[(700, '700MHz'),(270, '270MHz')]
    test_frequency_in_MHz = forms.FloatField()
    cutoff_frequency_in_MHz = forms.ChoiceField(choices=cutoff_choices, widget=forms.Select)
    high_pass_filter = forms.ChoiceField(choices=filter_choices, widget=forms.Select)



class INPUTRES(forms.ModelForm):
    class Meta():
        model = RES
        fields = '__all__'
