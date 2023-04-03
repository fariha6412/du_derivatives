from django.shortcuts import render

def home(request):
    return render(request, 'homepage.html')

def profile(request):
    return render(request, 'profile.html')

def login(request):
    return render(request, 'login.html')