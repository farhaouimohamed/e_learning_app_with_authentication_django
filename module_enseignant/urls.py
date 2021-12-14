from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('travailE/addtravailE', views.ajouter_travailE, name='ajouter_travail_a_rendre'),
    path('travailE/listtravailE', views.list_TravailE, name='list_travail_rendu'),
    path('update_travailE/<str:pk>/', views.updateTravailE, name="update_travailE"),
    path('delete_travailE/<str:pk>/', views.deletetravailE, name="delete_travailE"),

    path('etudiants/', views.list_etudiants, name='liste etudiants'),
    path('etudiants/addEtudiant', views.register_student, name='ajouter_etudiant'),
    path('delete_etudiant/<str:pk>/', views.deleteEtudiant, name="delete_etudiant"),
    path('detail_etudiant/<str:pk>/', views.detailEtudiant, name="detail_etudiant"),

    path('groupe/listGroupe', views.list_groupes, name='liste_groupes'),
    path('groupe/addGroupe', views.addGroupe, name="ajouter_groupe"),
    path('delete_groupe/<str:pk>/', views.deleteGroupe, name="delete_groupe"),

    path('module/listModule', views.list_modules, name='liste_modules'),
    path('module/addModule', views.addModule, name="add_module"),
    path('add_groupe_for_module/<str:pk>/', views.addGroupeForModule, name="add_groupe_for_module"),
    path('detail_module/<str:pk>/', views.detail_module, name="detail_module"),

    path('seances/', views.list_seances, name='liste_seances'),
    path('seances/addSeance', views.addSeance, name='add_seance'),
    path('delete_seance/<str:pk>/', views.deleteSeance, name='delete_seance'),
    path('detail__seance/<str:pk>/', views.detail__seance, name='detail__seance'),
    path('update_motif/<str:pk>/', views.update_motif, name='update_motif'),
]

