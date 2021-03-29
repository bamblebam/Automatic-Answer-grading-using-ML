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
    questions_created = Question.objects.filter(author=user)
    questions_responded = Response.objects.filter(user=user)
    context = {
        'questions': questions_created,
        'responses': questions_responded
    }
    return render(request, 'custom/dashboard.html', context=context)
