from django.shortcuts import render

# Create your views here.


def Home(request):
    return render(request, "custom/home.html")


def navbar(request):
    return render(request, "custom/navbar.html")