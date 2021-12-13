from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.pageAcceuil, name='acceuil'),
    path('etudiant/login', views.login_view, name='login_student'),
    path('enseignant/', views.register_enseignant, name='register_enseignant'),
    path('enseignant/login', views.login_enseignant, name='login_enseignant'),
    path('logout/', views.logout_view, name='logout')
]