from django.conf.urls import url
from django.urls import path
from module_etudiant import views


urlpatterns = [
    path('seances/', views.list_seances, name='liste_seances'),
    path('detail_seance/<str:pk>/', views.detail_seance, name='detail_seance'),
    path('rendre_travailR/<str:pk>/', views.rendre_travailR, name="rendre_travail"),
]

