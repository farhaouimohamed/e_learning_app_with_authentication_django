from django.conf.urls import url
from django.urls import path
from dashboard import views

urlpatterns = [
    path('dash_etudiant', views.taux_absenteisme, name='dash_etudiant'),
]

