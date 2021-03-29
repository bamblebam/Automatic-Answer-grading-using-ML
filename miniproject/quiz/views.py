# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Question, Response
from .forms import NewQuestionForm, NewResponseForm

# Create your views here.


@login_required()  # Teacher boolean
def newQuestionPage(request):
    form = NewQuestionForm()

    if request.method == 'POST':
        try:
            form = NewQuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.author = request.user
                question.save()
                return redirect("home")
        except Exception as e:
            print(e)
            raise

    context = {'form': form}
    return render(request, 'new-question.html', context)


def homePage(request):
    questions = Question.objects.all()
    context = {
        'questions': questions
    }
    return render(request, 'homepage.html', context)


def questionPage(request, id):
    response_form = NewResponseForm()

    if request.method == 'POST':
        try:
            response_form = NewResponseForm(request.POST)
            if response_form.is_valid():
                response = response_form.save(commit=False)
                response.user = request.user
                response.question = Question(id=id)
                response.save()

                return redirect('/question/'+str(id)+'#'+str(response.id))
        except Exception as e:
            print(e)
            raise

    question = Question.objects.get(id=id)
    context = {
        'question': question,
        'response_form': response_form,

    }
    return render(request, 'question.html', context)
