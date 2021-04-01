# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Question, Response
from .decorator import is_teacher
from .forms import NewQuestionForm, NewResponseForm, ResponseUpdateForm
from django_filters.views import FilterView
from django.views.generic import ListView, UpdateView
from django.core.exceptions import PermissionDenied
from .filters import QuestionFilter
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Create your views here.


class QuestionListView(FilterView):
    model = Question
    paginate_by = 10
    template_name = "quiz/question_home.html"
    filterset_class = QuestionFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request_copy = self.request.GET.copy()
        params = request_copy.pop('page', True) and request_copy.urlencode()
        context['params'] = params
        return context


class QuestionResponseView(ListView):
    model = Response
    paginate_by = 10
    template_name = 'quiz/responses.html'

    def get_queryset(self):
        responses = super().get_queryset()
        return responses.filter(question=Question.objects.get(slug=self.kwargs.get('slug')))


class ResponseUpdateView(UpdateView):
    model = Response
    form_class = ResponseUpdateForm
    template_name = 'quiz/response_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question"] = self.object.question
        return context


@login_required
@is_teacher
def newQuestionPage(request):
    form = NewQuestionForm()

    if request.method == 'POST':
        try:
            form = NewQuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.author = request.user
                question.save()
                return redirect("quiz-home")
        except Exception as e:
            print(e)
            raise

    context = {'form': form}
    return render(request, 'quiz/new-question.html', context)


@login_required
def questionPage(request, slug):
    question_answer = Question.objects.get(
        slug=slug).responses.filter(user=request.user)
    if len(question_answer) > 0:
        raise PermissionDenied
    response_form = NewResponseForm()
    if request.method == 'POST':
        try:
            response_form = NewResponseForm(request.POST)
            if response_form.is_valid():
                sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
                response_answer = response_form.cleaned_data['body']
                model_answer = Question.objects.get(slug=slug).model_answer
                sentence_embeddings = sbert_model.encode(
                    [model_answer, response_answer])
                score = cosine_similarity(sentence_embeddings)[0][1]
                response = response_form.save(commit=False)
                response.marks = round(score*100)
                response.user = request.user
                response.question = Question.objects.get(slug=slug)
                response.save()
                print(score)
                return redirect('quiz-home')
        except Exception as e:
            print(e)
            raise

    question = Question.objects.get(slug=slug)
    context = {
        'question': question,
        'response_form': response_form,
    }
    return render(request, 'quiz/question.html', context)
