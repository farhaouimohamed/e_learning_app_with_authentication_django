from django.db import models
from django.conf import settings

class Groupe(models.Model):
    identifiant=models.AutoField(primary_key=True,null=False)
    nom=models.CharField(max_length=255)
    nbr_etudiants=models.IntegerField(null=False,blank=False)
    amil_groupe=models.CharField(max_length=255)
    niveau_etude=models.CharField(max_length=255)

class Module(models.Model):
    nom=models.CharField(max_length=255, unique=True)
    nbr_heures_totale=models.IntegerField(null=False,blank=False)
    type=models.CharField(max_length=255)
    niveau=models.CharField(max_length=255)
    groupes=models.ManyToManyField(Groupe)
    enseignant=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
# Create your models here.
class TravailE(models.Model):
    identifiant=models.AutoField(primary_key=True,null=False)
    titre=models.CharField(max_length=255)
    date_lancement=models.DateField()
    date_retour=models.DateField()
    nature=models.CharField(max_length=255)
    descriptif=models.CharField(max_length=255)
    piece_jointe_enonce=models.URLField(max_length = 255)
    etat=models.CharField(max_length=255)
    module=models.ForeignKey(Module,on_delete=models.CASCADE)

class Seance(models.Model):
    identifiant=models.AutoField(primary_key=True,null=False)
    heure_debut=models.DateTimeField()
    heure_fin=models.DateTimeField()
    numero_salle=models.IntegerField(null=False,blank=False)
    objectif=models.CharField(max_length=255)
    resume=models.CharField(max_length=255)
    type=models.CharField(max_length=255)
    etat=models.CharField(max_length=255)
    module=models.ForeignKey(Module, on_delete=models.CASCADE)

class Absence(models.Model):
    identifiant=models.AutoField(primary_key=True,null=False)
    date=models.DateField()
    motif=models.CharField(max_length=255)
    justificatif=models.CharField(max_length=255)
    etudiant=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    seance=models.ForeignKey(Seance,on_delete=models.CASCADE)
class Enregistrement(models.Model):
    identifiant=models.AutoField(primary_key=True,null=False)
    nom=models.CharField(max_length=255, unique=True)
    url=models.CharField(max_length=255)
    contenu=models.CharField(max_length=255)
    type=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    date=models.DateField()
    seance=models.ForeignKey(Seance,on_delete=models.CASCADE)

# Create your models here.
class TravailR(models.Model):
    identifiant=models.AutoField(primary_key=True,null=False)
    piece_jointe_rendu=models.URLField(max_length = 255)
    evaluation=models.CharField(max_length=255)
    date=models.DateField(max_length=255)
    travailE = models.ForeignKey(TravailE,on_delete=models.CASCADE)
    etudiant=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
