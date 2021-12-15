from django.shortcuts import render, redirect
from django.http.response import JsonResponse

from module_enseignant.models import Groupe, Module, Seance, TravailE, TravailR
from account.models import Account
from module_etudiant.forms import TravailRModelForm

from datetime import date

def profil(request):
    user = request.user
    if user.is_authenticated:
        if user.is_student == True:
            etudiant = Account.objects.get(id=user.id)
            return render(request, "profil/profil.html",{"etudiant":etudiant})
        else:
            return JsonResponse("Vous n'avez pas d'accés sur cette page !!!!",safe=False)
    else:
        return render(request, "account/login_etudiant.html",{})

# Create your views here.
def list_seances(request):
    user = request.user
    if user.is_authenticated:
        if user.is_student == True:
            groupe = Groupe.objects.get(identifiant=user.groupe_id)
            print(groupe)
            modules = groupe.module_set.all()
            seances = []
            for module in modules:
                seances.extend(list(Seance.objects.filter(module_id=module.id)))
            return render(request, "seance/listSeance.html",{"seances":seances})
        else:
            return JsonResponse("Vous n'avez pas d'accés sur cette page !!!!",safe=False)
    else:
        return render(request, "account/login_etudiant.html",{})

def detail_seance(request, pk):
    user = request.user
    if user.is_authenticated:
        if user.is_student == True:
            seance = Seance.objects.get(identifiant=pk)
            module = Module.objects.get(id=seance.module_id)
            enseignant = Account.objects.get(id=module.enseignant_id)
            travauxEnonces = TravailE.objects.filter(module_id=module.id)
            context = {'module':module,'enseignant':enseignant,'travauxEnonces':travauxEnonces,'seance':seance}
            return render(request, "seance/detailSeancee.html",context)
        else:
            return JsonResponse("Vous n'avez pas d'accés sur cette page !!!!",safe=False)
    else:
        return render(request, "account/login_etudiant.html",{})
   
def rendre_travailR(request, pk):
    user = request.user
    if user.is_authenticated:
        if user.is_student == True:
            travailE = TravailE.objects.get(identifiant=pk)
            if request.method == 'POST':
                form = TravailRModelForm(request.POST,request.FILES)
                if form.is_valid():
                    travailsR = TravailR.objects.filter(travailE_id=travailE.identifiant)
                    travailR = TravailR()
                    print(user.id)
                    for t in travailsR:
                        if t.etudiant_id == user.id:
                            travailR = t
                    travailR.piece_jointe_rendu = request.FILES['piece_jointe_rendu']
                    travailR.date = date.today()   
                    travailR.is_terminated = True
                    travailR.etudiant_id = user.id
                    travailR.travailE = travailE
                    travailR.save()
                return redirect("/module_etudiant/seances")
            else: 
                form = TravailRModelForm()
                context = {'form':form,'travailE':travailE}
                return render(request, "travailR/rendreTravailR.html",context)
        else:
            return JsonResponse("Vous n'avez pas d'accés sur cette page !!!!",safe=False)
    else:
        return render(request, "account/login_etudiant.html",{})