from django.contrib import messages
from django.contrib.auth import logout
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from account.forms import RegistraionStudentForm
from account.models import Account
from module_enseignant.forms import GroupeModelForm, ModuleModelForm, SeanceModelForm
from module_etudiant.forms import TravailRModelForm

from module_enseignant.models import Absence, Groupe, Module, Seance, TravailE, TravailR
from module_enseignant.forms import TravailEModelForm
from datetime import datetime
  

######################################################## TravailE ##############################
def list_TravailE(request):
   context = {}
   user = request.user
   if user.is_authenticated:
       if user.is_student == False:
            modules = Module.objects.filter(enseignant_id=user.id)
            travailEnonces = []
            for module in modules:
                travailEnonces.extend(list(TravailE.objects.filter(module_id=module.id)))
            return render(request, "TravailE/listTravailE.html",{"travailEnonces": travailEnonces})
       else:
           return JsonResponse("Vous n'avez pas d'accés sur cette page !!!!",safe=False)
   else:
       return render(request, "account/login_enseignant.html",{})

def updateTravailE(request,pk):
    user = request.user
    if user.is_authenticated:
        if user.is_student == False:
            travailE = TravailE.objects.get(identifiant=pk)
            form = TravailRModelForm(instance=travailE)
            if request.method == 'POST':
                form = TravailRModelForm(request.POST, instance=travailE)
                if form.is_valid():
                    if form.is_valid():
                        form.save()
                        return redirect("/module_enseignant/travailE/listtravailE")
            context = {'form':form}
            return render(request, "travailE/addTravailE.html", context)
        else:
            return JsonResponse("Vous n'avez pas d'accés sur cette page !!!!",safe=False)
    else:
        return render(request, "account/login_enseignant.html",{})


def deletetravailE(request,pk):
    user = request.user
    if user.is_authenticated:
        if user.is_student == False:
            travailE = TravailE.objects.get(identifiant=pk)
            travailE.delete()
            return redirect("/module_enseignant/travailE/listtravailE")
        else:
            return JsonResponse("Vous n'avez pas d'accés sur cette page !!!!",safe=False)
    else:
        return render(request, "account/login_enseignant.html",{})
    
def ajouter_travailE(request):
    user = request.user
    if user.is_authenticated:
        if user.is_student == False:
            if request.method == 'POST':
                form = TravailEModelForm(request.POST, request.FILES)
                if form.is_valid():
                    module = Module()
                    id_module = request.POST['inputNomModule']
                    module = Module.objects.get(id=id_module)
                    travailE = form.save(commit=False)
                    travailE.module = module
                    travailE.save()
                    add_init_travailR(id_module,travailE)
                    return redirect("/module_enseignant/travailE/listtravailE")
            else:
                modules = Module.objects.filter(enseignant_id=user.id)
                form=TravailEModelForm()
                return render(request, "travailE/addTravailE.html",{"form":form,"modules":modules})
        else:
            return JsonResponse("Vous n'avez pas d'accés sur cette page !!!!",safe=False)
    else:
        return render(request, "account/login_enseignant.html",{})

def add_init_travailR(module_id,travailE):
    module = Module.objects.get(id=module_id)
    groupes = module.groupes.all()
    etudiants = []
    for groupe in groupes:
        etudiants.extend(list(Account.objects.filter(groupe_id=groupe.identifiant)))
    for etudiant in etudiants:
        travailR = TravailR()
        travailR.etudiant = etudiant
        travailR.travailE = travailE
        travailR.save()



#####################################################################################################


######################################################## Etudiant ##############################

def list_etudiants(request):
    user = request.user
    if user.is_authenticated:
        if user.is_student == False:
            etudiants = Account.objects.filter(is_student=True)
            return render(request, "etudiant/listEtudiant.html",{"etudiants":etudiants})
        else:
            return JsonResponse("Vous n'avez pas d'accés sur cette page !!!!",safe=False)
    else:
       return render(request, "account/login_enseignant.html",{})


def register_student(request):
    user = request.user
    if user.is_authenticated:
        if user.is_student == False:
            if request.method == 'GET':
                groupes = Groupe.objects.all()
                form = RegistraionStudentForm()
                context = {'form':form, 'groupes':groupes}
                return render(request, 'etudiant/register_student.html', context)
            if request.method == 'POST':
                form = RegistraionStudentForm(request.POST, request.FILES)
                if form.is_valid():
                    id_groupe = request.POST['inputNomGroupe']
                    groupe = Groupe.objects.get(identifiant=id_groupe)
                    account = Account()
                    account = form.save(commit=False)
                    account.is_student = True
                    account.groupe = groupe
                    account.save()
                    user = form.cleaned_data.get('nom')
                    messages.success(request, 'Account was created for ' + user)
                    return redirect('/module_enseignant/etudiants/')
                else:
                    print('Form is not valid')
                    messages.error(request, 'Error Processing your request')
                    context = {'form':form}
                    return render(request, 'etudiant/register_student.html',context)
            return render(request, 'etudiant/register_student.html', {})
        else:
            return JsonResponse("Vous n'avez pas d'accés sur cette page !!!!",safe=False)
    else:
        return render(request, "account/login_enseignant.html",{})

def deleteEtudiant(request, pk):
    user = request.user
    if user.is_authenticated:
        if user.is_student == False:
            etudiant = Account.objects.get(id=pk)
            if request.method == 'POST':
                etudiant.delete()
                return redirect("/etudiants")
            context = {'item':etudiant}
            return render(request, 'e_learning_platform/delete.html', context)
        else:
            return JsonResponse("Vous n'avez pas d'accés sur cette page !!!!",safe=False)
    else:
       return render(request, "account/login_enseignant.html",{})

def detailEtudiant(request, pk):
    user = request.user
    if user.is_authenticated:
        if user.is_student == False:
            etudiant = Account.objects.get(id=pk)
            context = {'etudiant':etudiant}
            return render(request, 'etudiant/detailEtudiant.html', context)
        else:
            return JsonResponse("Vous n'avez pas d'accés sur cette page !!!!",safe=False)
    else:
       return render(request, "account/login_enseignant.html",{})
#####################################################################################################

################################################ Groupe #############################################

def list_groupes(request):
    user = request.user
    if user.is_authenticated:
        if user.is_student == False:
            groupes = Groupe.objects.all()
            return render(request, "groupe/listGroupe.html",{"groupes":groupes})
        else:
            return JsonResponse("Vous n'avez pas d'accés sur cette page !!!!",safe=False)
    else:
       return render(request, "account/login_enseignant.html",{})

def addGroupe(request):
    user = request.user
    if user.is_authenticated:
        if user.is_student == False:
            if request.method == 'POST':
                form = GroupeModelForm(request.POST)
                if form.is_valid():
                    groupe = form.save(commit=False)
                    groupe.save()
                return redirect("/module_enseignant/groupe/listGroupe")
            else:
                groupeForm=GroupeModelForm()
                return render(request, "groupe/addGroupe.html",{"groupeForm":groupeForm})
        else:
            return JsonResponse("Vous n'avez pas d'accés sur cette page !!!!",safe=False)
    else:
        return render(request, "account/login_enseignant.html",{})

def deleteGroupe(request, pk):
    user = request.user
    if user.is_authenticated:
        if user.is_student == False:
            groupe = Groupe.objects.get(identifiant=pk)
            groupe.delete()
            return redirect("/module_enseignant/groupe/listGroupe")
        else:
            return JsonResponse("Vous n'avez pas d'accés sur cette page !!!!",safe=False)
    else:
       return render(request, "account/login_enseignant.html",{})

#####################################################################################################


########################################### Module ##################################################

def detail_module(request,pk):
    user = request.user
    if user.is_authenticated:
        if user.is_student == False:
            module = Module.objects.get(id=pk)
            groupes = module.groupes.all()
            return render(request, "module/detailModule.html",{"module":module, 'groupes':groupes})
        else:
            return JsonResponse("Vous n'avez pas d'accés sur cette page !!!!",safe=False)
    else:
       return render(request, "account/login_enseignant.html",{})


def list_modules(request):
    user = request.user
    if user.is_authenticated:
        if user.is_student == False:
            modules = Module.objects.filter(enseignant_id=user.id)
            return render(request, "module/listModule.html",{"modules":modules})
        else:
            return JsonResponse("Vous n'avez pas d'accés sur cette page !!!!",safe=False)
    else:
       return render(request, "account/login_enseignant.html",{})
def addModule(request):
    user = request.user
    if user.is_authenticated:
        if user.is_student == False:
            if request.method == 'POST':
                form = ModuleModelForm(request.POST)
                if form.is_valid():
                    enseignant = Account.objects.get(id=user.id)
                    module = Module()
                    module = form.save(commit=False)
                    module.enseignant = enseignant
                    module.save()
                return redirect("/module_enseignant/module/listModule")
            else:
                moduleForm=ModuleModelForm()
                return render(request, "module/addModule.html",{"moduleForm":moduleForm})
        else:
            return JsonResponse("Vous n'avez pas d'accés sur cette page !!!!",safe=False)
    else:
        return render(request, "account/login_enseignant.html",{})


def addGroupeForModule(request, pk):
    user = request.user
    if user.is_authenticated:
        if user.is_student == False:
            module = Module.objects.get(id=pk)
            form = ModuleModelForm(instance=module)
            if request.method == 'POST':
                id_groupe = request.POST['inputNomGroupe']
                groupe = Groupe.objects.get(identifiant=id_groupe)
                module = form.save(commit=False)
                module.groupes.add(groupe)
                module.save()
                return redirect("/module_enseignant/module/listModule")
            groupes = Groupe.objects.all()
            context = {'moduleForm':form, 'groupes':groupes}
            return render(request, "groupe/addGroupeForModule.html",context)
        else:
            return JsonResponse("Vous n'avez pas d'accés sur cette page !!!!",safe=False)
    else:
        return render(request, "account/login_enseignant.html",{})

#####################################################################################################


############################################## Seance ###############################################

def list_seances(request):
    user = request.user
    if user.is_authenticated:
        if user.is_student == False:
            modules = Module.objects.filter(enseignant_id=user.id)
            seances = []
            for module in modules:
                seances.extend(list(Seance.objects.filter(module_id=module.id)))
            return render(request, "seance/listSeances.html",{"seances":seances})
        else:
            return JsonResponse("Vous n'avez pas d'accés sur cette page !!!!",safe=False)
    else:
        return render(request, "account/login_enseignant.html",{})

def detail__seance(request,pk):
    user = request.user
    if user.is_authenticated:
        if user.is_student == False:
            seance = Seance.objects.get(identifiant=pk)
            absences = seance.absence_set.all()
            return render(request, "seance/detailSeance.html",{"absences":absences,"seance":seance})
        else:
            return JsonResponse("Vous n'avez pas d'accés sur cette page !!!!",safe=False)
    else:
        return render(request, "account/login_enseignant.html",{})
    
def update_motif(request,pk):
    user = request.user
    if user.is_authenticated:
        if user.is_student == False:
            absence = Absence.objects.get(identifiant=pk)
            etudiant = Account.objects.get(id=absence.etudiant_id)
            if request.method == 'POST':
                motif = request.POST['inputMotif']
                justificatif = request.POST['inputJustificatif']
                absence.motif = motif
                absence.justificatif = justificatif
                absence.save()
                return redirect("/module_enseignant/seances")
            context = {'absence':absence,'etudiant':etudiant}
            return render(request, "seance/update_motif.html",context)
        else:
            return JsonResponse("Vous n'avez pas d'accés sur cette page !!!!",safe=False)
    else:
        return render(request, "account/login_enseignant.html",{})
   
def addSeance(request):
    user = request.user
    if user.is_authenticated:
        if user.is_student == False:
            if request.method == 'POST':
                form = SeanceModelForm(request.POST)
                if form.is_valid():
                    id_module = request.POST.get('inputNomModule')
                    module = Module.objects.get(id=id_module)
                    groupes = module.groupes.all()
                    etudiants = []
                    for groupe in groupes:
                        etudiants.extend(list(Account.objects.filter(groupe_id=groupe.identifiant)))
                    seance = Seance()
                    seance = form.save(commit=False)
                    seance.module = module
                    seance.save()
                    for etudiant in etudiants:
                        absence = Absence(date=datetime.now(),motif="absent",seance=seance,etudiant=etudiant)
                        absence.save()
                return redirect("/module_enseignant/seances")
            else:
                modules = Module.objects.filter(enseignant_id=user.id)
                seanceForm=SeanceModelForm()
                return render(request, "seance/addSeance.html",{"seanceForm":seanceForm,'modules':modules})
        else:
            return JsonResponse("Vous n'avez pas d'accés sur cette page !!!!",safe=False)
    else:
        return render(request, "account/login_enseignant.html",{})

def deleteSeance(request, pk):
    user = request.user
    if user.is_authenticated:
        if user.is_student == False:
            seance = Seance.objects.get(identifiant=pk)
            seance.delete()
            return redirect("/module_enseignant/seances")
        else:
            return JsonResponse("Vous n'avez pas d'accés sur cette page !!!!",safe=False)
    else:
        return render(request, "account/login_enseignant.html",{})
   
#####################################################################################################