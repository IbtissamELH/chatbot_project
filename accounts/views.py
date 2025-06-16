from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
         login(request, user)
         messages.success(request, f"Bienvenue {user.username}, vous êtes maintenant connecté.")
         return redirect('home')
        else:
            messages.error(request, 'Identifiants invalides')
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect('login')
    

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        User.objects.create_user(username=username, email=email, password=password)
        user = authenticate(request, username=username, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'accounts/register.html')
