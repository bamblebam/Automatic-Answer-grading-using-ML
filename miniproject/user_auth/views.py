from django.shortcuts import render

# Create your views here.


def Home(request):
    return render(request, "custom/home.html")


def signup(request):
    return render(request, "account/signup.html")


def login(request):
    return render(request, "account/login.html")


def logout(request):
    return render(request, "account/logout.html")
