from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from module_enseignant.models import Groupe, Module


class MyAccountManager(BaseUserManager):
	def create_user(self, email,email_per, nbr_heures_totale, photo, nom, prenom, date_naissance,etat,situation, password=None,is_student=False):
		if not email:
			raise ValueError('Users must have an email address')
		if not nom:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
            email_per=self.normalize_email(email_per),
            nbr_heures_totale=nbr_heures_totale,
            photo=photo,
			nom=nom,
            prenom=prenom,
            date_naissance=date_naissance,
            etat=etat,
            situation=situation,
            is_student=is_student,
		)       
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email,email_per, nbr_heures_totale, photo, nom, prenom, date_naissance,etat,situation, password=None,is_student=False):
		user = self.create_user(
            self, email,email_per, nbr_heures_totale, photo, nom, prenom, date_naissance,etat,situation, password,is_student
        )
		user.is_responsable = True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    email=models.EmailField(verbose_name="email", max_length=60, unique=True)
    email_per=models.EmailField(verbose_name="email_per", max_length=60)
    nbr_heures_totale=models.IntegerField(null=True,blank=True)
    date_joined=models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login=models.DateTimeField(verbose_name='last login', auto_now=True)
    photo=models.ImageField(null=True, blank=True)
    date_naissance=models.DateField(null=True, blank=True)
    etat=models.CharField(max_length=255, null=True, blank=True)
    situation=models.CharField(max_length=255, null=True, blank=True)
    groupe=models.ForeignKey(Groupe,on_delete=models.CASCADE, null=True, blank=True)
    is_responsable			= models.BooleanField(default=False)
    is_active				= models.BooleanField(default=True)
    is_student				= models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom']

    objects = MyAccountManager()
    









