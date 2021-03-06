from django.http.response import JsonResponse
from django.shortcuts import render
from account.models import Account

import json

from module_enseignant.models import Absence, Groupe, Module, Seance, TravailE, TravailR

# Create your views here.




############################################# dash absenteisme #####################
def taux_absenteisme(request):
    user = request.user
    if user.is_authenticated:
        if user.is_student == False:
            if request.method == 'POST':
                data = [0,0,0,0]
                if 'inputNomEtudiant' in request.POST:
                    data = filter_with_etudiant(request.POST['inputNomEtudiant'])
                    print(data)
                elif 'inputNomModule' in request.POST:
                    data = filter_with_module(request.POST['inputNomModule'])
                    print(data)
                elif 'inputNomGroupe' in request.POST:
                    data = filter_with_groupe(request.POST['inputNomGroupe'])
                    print(data)
                context = getInitialContext(user.id,data)
                return render(request, 'suiviTauxAbs.html',context)
            context = getInitialContext(user.id,[0,0,0,0])
            return render(request, 'suiviTauxAbs.html',context)
        else:
            return JsonResponse("Vous n'avez pas d'accés sur cette page !!!!",safe=False)
    else:
        return render(request, "account/login_enseignant.html",{})
    
def getInitialContext(id,data):
    modules = modules = Module.objects.filter(enseignant_id=id)
    groupes = []
    for module in modules:
        groupes.extend(module.groupes.all())
    groupes = list(set(groupes))
    etudiants = []
    for groupe in groupes:
        etudiants.extend(list(Account.objects.filter(groupe_id=groupe.identifiant)))
    context = {"modules":modules,"groupes":groupes,"etudiants":etudiants,"datas":json.dumps(data)}
    return context

def filter_with_module(id_module):
    module = Module.objects.get(id=id_module)
    seances = Seance.objects.filter(module_id=module.id)
    absences = []
    for seance in seances:
        absences.extend(list(Absence.objects.filter(seance_id=seance.identifiant)))
    data = [0,0,0,0]
    for absence in absences:
        if absence.motif == 'present':
            data[0] += 1
        if absence.motif == 'absent':
            data[1] += 1
        if absence.motif == 'exclu':
            data[2] += 1
        if absence.motif == 'retard':
            data[3] += 1
    return data

def filter_with_etudiant(id_etudiant):
    absences = Absence.objects.filter(etudiant_id=id_etudiant)
    data = [0,0,0,0]
    for absence in absences:
        if absence.motif == 'present':
            data[0] += 1
        if absence.motif == 'absent':
            data[1] += 1
        if absence.motif == 'exclu':
            data[2] += 1
        if absence.motif == 'retard':
            data[3] += 1
    return data

def filter_with_groupe(id_groupe):
    etudiants = Account.objects.filter(groupe_id = id_groupe)
    absences = []
    for etudiant in etudiants:
        absences.extend(list(Absence.objects.filter(etudiant_id=etudiant.id)))
    data = [0,0,0,0]
    for absence in absences:
        if absence.motif == 'present':
            data[0] += 1
        if absence.motif == 'absent':
            data[1] += 1
        if absence.motif == 'exclu':
            data[2] += 1
        if absence.motif == 'retard':
            data[3] += 1
    return data


############################################# dash TravailR #####################
def taux_travail_rendus(request):
    user = request.user
    if user.is_authenticated:
        if user.is_student == False:
            if request.method == 'POST':
                data = [0,0]
                if 'inputNomEtudiant' in request.POST:
                    data = filter_t_with_etudiant(request.POST['inputNomEtudiant'])
                    print(data)
                elif 'inputNomModule' in request.POST:
                    data = filter_t_with_module(request.POST['inputNomModule'])
                    print(data)
                elif 'inputNomGroupe' in request.POST:
                    data = filter_t_with_groupe(request.POST['inputNomGroupe'])
                    print(data)
                context = getInitialContextT(user.id,data)
                return render(request, 'suiviTravailR.html',context)
            context = getInitialContextT(user.id,[0,0])
            return render(request, 'suiviTravailR.html',context)
        else:
            return JsonResponse("Vous n'avez pas d'accés sur cette page !!!!",safe=False)
    else:
        return render(request, "account/login_enseignant.html",{})


def filter_t_with_etudiant(id_etudiant):
    travailsR = TravailR.objects.filter(etudiant_id=id_etudiant)
    data = [0,0]
    for travailR in travailsR:
        if travailR.is_terminated == True:
            data[0] += 1
        else:
            data[1] += 1
    return data


def filter_t_with_module(id_module):
    module = Module.objects.get(id=id_module)

    travailsE = TravailE.objects.filter(module_id=module.id)
    travailsR = []
    for travailE in travailsE:
        travailsR.extend(list(TravailR.objects.filter(travailE_id=travailE.identifiant)))
    data = [0,0]
    for travailR in travailsR:
        if travailR.is_terminated == True:
            data[0] += 1
        else:
            data[1] += 1
    return data

def filter_t_with_groupe(id_groupe):
    etudiants = Account.objects.filter(groupe_id = id_groupe)
    travailsR = []
    for etudiant in etudiants:
        travailsR.extend(list(TravailR.objects.filter(etudiant_id=etudiant.id)))
    data = [0,0]
    for travailR in travailsR:
        if travailR.is_terminated == True:
            data[0] += 1
        else:
            data[1] += 1
    return data


def getInitialContextT(id,data):
    modules = modules = Module.objects.filter(enseignant_id=id)
    groupes = []
    for module in modules:
        groupes.extend(module.groupes.all())
    groupes = list(set(groupes))
    etudiants = []
    for groupe in groupes:
        etudiants.extend(list(Account.objects.filter(groupe_id=groupe.identifiant)))
    context = {"modules":modules,"groupes":groupes,"etudiants":etudiants,"datas":json.dumps(data)}
    return context