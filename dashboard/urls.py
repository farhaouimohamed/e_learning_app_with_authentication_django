from django.conf.urls import url
from django.urls import path
from dashboard import views

urlpatterns = [
    path('dash_etudiant', views.taux_absenteisme, name='dash_etudiant'),
    path('dash_travailr', views.taux_travail_rendus, name='dash_travailr'),
]

