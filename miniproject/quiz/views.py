# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Question, Response
from .forms import NewQuestionForm, NewResponseForm
from django_filters.views import FilterView
from .filters import QuestionFilter

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
    return render(request, 'quiz/new-question.html', context)


# def homePage(request):
#     questions = Question.objects.all()
#     context = {
#         'questions': questions
#     }
#     return render(request, 'homepage.html', context)


class QuestionListView(FilterView):
    model = Question
    paginate_by = 10
    template_name = "quiz/question_home.html"
    filterset_class = QuestionFilter


def questionPage(request, slug):
    response_form = NewResponseForm()

    if request.method == 'POST':
        try:
            response_form = NewResponseForm(request.POST)
            if response_form.is_valid():
                response = response_form.save(commit=False)
                response.user = request.user
                response.question = Question.objects.get(slug=slug)
                response.save()
                return redirect('home')
        except Exception as e:
            print(e)
            raise

    question = Question.objects.get(slug=slug)
    context = {
        'question': question,
        'response_form': response_form,

    }
    return render(request, 'quiz/question.html', context)
