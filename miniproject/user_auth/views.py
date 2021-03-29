from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from quiz.models import Question, Response
from .models import User
# Create your views here.


def Home(request):
    return render(request, "custom/home.html")


@login_required
def dashboard(request):
    user = request.user
    questions_created = Question.objects.filter(
        author=user).order_by("-date_added")
    questions_responded = Response.objects.filter(
        user=user).order_by("-date_added")
    context = {
        'questions': questions_created,
        'responses': questions_responded
    }
    return render(request, 'custom/dashboard.html', context=context)
