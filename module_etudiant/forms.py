from django import forms
from django.forms import fields

from module_enseignant.models import TravailR

class TravailRModelForm(forms.ModelForm):
    class Meta:
        model = TravailR
        fields = ('piece_jointe_rendu',)
        widgets = {
            'piece_jointe_rendu':forms.FileInput(attrs={'class':'form-control'})
        }