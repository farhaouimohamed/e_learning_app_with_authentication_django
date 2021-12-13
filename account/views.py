from django.http.response import JsonResponse
from django.shortcuts import render,redirect

from django.contrib.auth import login, authenticate, logout
import account

from account.forms import RegistraionEnseignantForm, RegistraionStudentForm, AccountAuthenticationForm, AccountUpdateForm

from django.contrib import messages

from account.models import Account


def register_enseignant(request):
    if request.method == 'GET':
        form = RegistraionEnseignantForm()
        context = {'form':form}
        return render(request, 'account/register_enseignant.html', context)
    if request.method == 'POST':
        form = RegistraionEnseignantForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('nom')
            messages.success(request, 'Account was created for ' + user)
            return redirect('/home')
        else:
            print('Form is not valid')
            messages.error(request, 'Error Processing your request')
            context = {'form':form}
            return render(request, 'account/register_enseignant.html',context)
    return render(request, 'account/register_enseignant.html', {})

def login_student(request):

	context = {}

	user = request.user
	if user.is_authenticated: 
		
		return redirect("/home")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				return redirect("/home")

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form

	return render(request, "account/login_etudiant.html", context)

def login_enseignant(request):
	context = {}

	user = request.user
	if user.is_authenticated: 
		return redirect("/module_enseignant/travailR/listtravailR")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				return redirect("/module_enseignant/travailR/listtravailR")

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form

	return render(request, "account/login_enseignant.html", context)

def pageAcceuil(request):
    return render(request, 'home.html',{})

def logout_view(request):
	logout(request)
	return redirect('/home')


def login_view(request):

	context = {}

	user = request.user
	if user.is_authenticated: 
		if user.is_student == True:
			print("********** etudiant")
		elif user.is_student == False:
			print(("********* enseignant"))
		else:
			print("//////////////")
		return redirect("/home")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				print("999")
				print(user)
				print(type(user))
				return redirect("/home")

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form

	# print(form)
	return render(request, "account/login_etudiant.html", context)


def account_view(request):

	if not request.user.is_authenticated:
			return redirect("login")

	context = {}
	if request.POST:
		form = AccountUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.initial = {
					"email": request.POST['email'],
					"username": request.POST['username'],
			}
			form.save()
			context['success_message'] = "Updated"
	else:
		form = AccountUpdateForm(

			initial={
					"email": request.user.email, 
					"username": request.user.username,
				}
			)

	context['account_form'] = form

	blog_posts = BlogPost.objects.filter(author=request.user)
	context['blog_posts'] = blog_posts

	return render(request, "account/account.html", context)


def must_authenticate_view(request):
	return render(request, 'account/must_authenticate.html', {})