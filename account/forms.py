from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.forms import widgets

from account.models import Account


class RegistraionEnseignantForm(UserCreationForm):

    class Meta:
        model = Account
        fields = ('email', 'password1','password2','nom','prenom','email_per','nbr_heures_totale','is_responsable')
        widgets = {
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'nom':forms.TextInput(attrs={'class':'form-control'}),
            'prenom':forms.TextInput(attrs={'class':'form-control'}),
            'email_per':forms.EmailInput(attrs={'class':'form-control'}),
            'nbr_heures_totale':forms.NumberInput(attrs={'class':'form-control'}),
            'is_responsable':forms.CheckboxInput(attrs={'class':'form-control'}),
			'password1':forms.PasswordInput(attrs={'class':'form-control'}),
			'password2':forms.PasswordInput(attrs={'class':'form-control'}),
        }
class RegistraionStudentForm(UserCreationForm):

    class Meta:
        model = Account
        fields = ('email','password1','password2', 'nom','prenom','photo','date_naissance','etat','situation')
        widgets = {
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'nom':forms.TextInput(attrs={'class':'form-control'}),
            'prenom':forms.TextInput(attrs={'class':'form-control'}),
            'photo':forms.FileInput(attrs={'class':'form-control'}),
            'date_naissance':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'etat':forms.TextInput(attrs={'class':'form-control'}),
            'situation':forms.TextInput(attrs={'class':'form-control'}),
			'password1':forms.PasswordInput(attrs={'class':'form-control'}),
			'password2':forms.PasswordInput(attrs={'class':'form-control'}),
        }

class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	email = forms.EmailField(label='Adresse mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))

	class Meta:
		model = Account
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")


class AccountUpdateForm(forms.ModelForm):

	class Meta:
		model = Account
		fields = ('email', 'nom', )

	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
		except Account.DoesNotExist:
			return email
		raise forms.ValidationError('Email "%s" is already in use.' % account)

	def clean_username(self):
		nom = self.cleaned_data['nom']
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(nom=nom)
		except Account.DoesNotExist:
			return nom
		raise forms.ValidationError('nom "%s" is already in use.' % nom)
