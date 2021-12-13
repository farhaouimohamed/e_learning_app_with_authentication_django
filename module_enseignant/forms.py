from django import forms
from django.forms import fields

from module_enseignant.models import Groupe, Module, Seance, TravailE


class TravailEModelForm(forms.ModelForm):
    class Meta:
        model = TravailE
        fields = ('titre','date_lancement','date_retour','nature','descriptif','etat','piece_jointe_enonce')
        widgets = {
            'titre':forms.TextInput(attrs={'class':'form-control'}),
            'date_retour':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'nature':forms.TextInput(attrs={'class':'form-control'}),
            'descriptif':forms.TextInput(attrs={'class':'form-control'}),
            'etat':forms.TextInput(attrs={'class':'form-control'}),
            'date_lancement':forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'piece_jointe_enonce':forms.FileInput(attrs={'class':'form-control'})
        }

class GroupeModelForm(forms.ModelForm):
    class Meta:
        model = Groupe
        fields = ('nom','nbr_etudiants','amil_groupe','niveau_etude')
        widgets = {
            'nom':forms.TextInput(attrs={'class':'form-control'}),
            'nbr_etudiants':forms.NumberInput(attrs={'class':'form-control'}),
            'amil_groupe':forms.TextInput(attrs={'class':'form-control'}),
            'niveau_etude':forms.TextInput(attrs={'class':'form-control'}),
        }


class ModuleModelForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ('nom','nbr_heures_totale','type','niveau')
        widgets = {
            'nom':forms.TextInput(attrs={'class':'form-control'}),
            'nbr_heures_totale':forms.NumberInput(attrs={'class':'form-control'}),
            'type':forms.TextInput(attrs={'class':'form-control'}),
            'niveau':forms.TextInput(attrs={'class':'form-control'}),
        }


class SeanceModelForm(forms.ModelForm):
    class Meta:
        model = Seance
        fields = ('heure_debut','heure_fin','numero_salle','objectif','resume','etat','type')
        widgets = {
            'heure_debut':forms.TimeInput(attrs={'class':'form-control','type':'datetime-local'}),
            'heure_fin':forms.TimeInput(attrs={'class':'form-control','type':'datetime-local'}),
            'numero_salle':forms.NumberInput(attrs={'class':'form-control'}),
            'objectif':forms.TextInput(attrs={'class':'form-control'}),
            'resume':forms.TextInput(attrs={'class':'form-control'}),
            'type':forms.TextInput(attrs={'class':'form-control'}),
            'etat':forms.TextInput(attrs={'class':'form-control'}),
        }

