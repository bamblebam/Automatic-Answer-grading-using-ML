# Create your views here.
from django.db.models.query import QuerySet
from django.http import request
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from .models import Question, Response, Exam, ExamResponse
from .decorator import is_teacher, question_answered, details_filled, question_private, IsTeacherMixin, ExamAnsweredMixin, DetailsFilledMixin
from .forms import NewQuestionForm, NewResponseForm, ResponseUpdateForm, ExamResponseForm, EmptyQueryBaseModelFormSet
from django_filters.views import FilterView
from django.views.generic import ListView, UpdateView, CreateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from .filters import QuestionFilter, ExamFilter
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Create your views here.


class QuestionListView(FilterView):
    model = Question
    paginate_by = 10
    template_name = "quiz/question_home.html"
    filterset_class = QuestionFilter

    def get_queryset(self):
        questions = super().get_queryset()
        return questions.filter(is_exam=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request_copy = self.request.GET.copy()
        params = request_copy.pop('page', True) and request_copy.urlencode()
        context['params'] = params
        return context


class ExamListView(FilterView):
    model = Exam
    paginate_by = 10
    template_name = "quiz/exam_home.html"
    filterset_class = ExamFilter

    def get_queryset(self):
        exams = super().get_queryset()
        return exams

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request_copy = self.request.GET.copy()
        params = request_copy.pop('page', True) and request_copy.urlencode()
        context['params'] = params
        return context


class QuestionResponseView(LoginRequiredMixin, IsTeacherMixin, UserPassesTestMixin, ListView):
    model = Response
    paginate_by = 10
    template_name = 'quiz/responses.html'

    def get_queryset(self):
        responses = super().get_queryset()
        return responses.filter(question=Question.objects.get(slug=self.kwargs.get('slug')))

    def test_func(self):
        if Question.objects.get(slug=self.kwargs.get('slug')).author == self.request.user:
            return True
        return False


class ResponseUpdateView(LoginRequiredMixin, IsTeacherMixin, UserPassesTestMixin, UpdateView):
    model = Response
    form_class = ResponseUpdateForm
    template_name = 'quiz/response_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question"] = self.object.question
        return context

    def test_func(self):
        if self.get_object().question.author == self.request.user:
            return True
        return False

    def get_success_url(self):
        return reverse('responses', kwargs={'slug': self.get_object().question.slug})


class ExamResponseView(LoginRequiredMixin, IsTeacherMixin, UserPassesTestMixin, ListView):
    model = ExamResponse
    paginate_by = 10
    template_name = 'quiz/exam_response.html'

    def get_queryset(self):
        responses = super().get_queryset()
        return responses.filter(exam=Exam.objects.get(slug=self.kwargs.get('slug')))

    def test_func(self):
        if Exam.objects.get(slug=self.kwargs.get('slug')).author == self.request.user:
            return True
        return False


class ExamResponseUpdateView(LoginRequiredMixin, IsTeacherMixin, UserPassesTestMixin, UpdateView):
    model = ExamResponse
    paginate_by = 10
    fields = ['marks']
    template_name = 'quiz/exam_response_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        responses = self.object.responses.all()
        questions = self.object.exam.questions.all()
        responded_questions = [response.question for response in responses]
        complete_response = list(responses).copy()
        for i, question in enumerate(questions):
            if question not in responded_questions:
                complete_response.insert(i, question)

        context['responses'] = complete_response
        return context

    def test_func(self):
        if self.get_object().exam.author == self.request.user:
            return True
        return False

    def get_success_url(self):
        return reverse('exam-responses', kwargs={'slug': self.get_object().exam.slug})


def private_check(request, slug):
    question = Question.objects.get(slug=slug)
    code = question.question_code
    if request.method == 'POST':
        input_code = request.POST.get('code')
        if code == input_code:
            return redirect('question', slug)
        else:
            raise PermissionDenied
    return render(request, 'quiz/privatequestion.html')


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
@question_answered
@details_filled
@question_private
def questionPage(request, slug):
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


def already_answered(request):
    return render(request, 'quiz/already_answered.html')


class CreateExam(LoginRequiredMixin, IsTeacherMixin, CreateView):
    model = Exam
    template_name = 'quiz/create_exam.html'
    fields = ['title', 'num_questions']
    context_object_name = 'exam'

    def form_valid(self, form):
        form.instance.save()
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('add-questions', kwargs={'slug': self.object.slug})


@login_required
@is_teacher
def addQuestionsToExam(request, slug):
    exam = get_object_or_404(Exam, slug=slug)
    ExamQuestionFormset = modelformset_factory(Question,
                                               form=NewQuestionForm, extra=exam.num_questions, can_order=True, formset=EmptyQueryBaseModelFormSet)
    if request.method == 'POST':
        formset = ExamQuestionFormset(request.POST)
        instances = formset.save()
        for instance in instances:
            instance.author = request.user
            instance.is_exam = True
            instance.save()
            exam.questions.add(instance)
            exam.save()
        return redirect('exam-home')
    else:
        formset = ExamQuestionFormset()

    context = {'formset': formset}
    return render(request, 'quiz/add_questions.html', context)


class CreateExamResponse(LoginRequiredMixin, DetailsFilledMixin, ExamAnsweredMixin, CreateView):
    model = ExamResponse
    fields = ['slug']
    template_name = 'quiz/create_examresponse.html'
    context_object_name = 'exam_response'

    def form_valid(self, form):
        form.instance.save()
        form.instance.user = self.request.user
        form.instance.exam = Exam.objects.get(slug=self.kwargs.get('slug'))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exam'] = Exam.objects.get(slug=self.kwargs.get('slug'))
        return context

    def get_success_url(self):
        return reverse('add-response', kwargs={'slug': self.object.slug})


@login_required
def addResponseToExam(request, slug):
    exam_response = get_object_or_404(ExamResponse, slug=slug)
    exam = exam_response.exam
    questions = exam.questions.all()
    ExamResponseFormset = modelformset_factory(Response, form=ExamResponseForm, extra=len(
        questions), can_order=True, formset=EmptyQueryBaseModelFormSet)
    if request.method == 'POST':
        formset = ExamResponseFormset(request.POST)
        sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
        total_marks = list()
        for form in formset:
            if form.is_valid():
                instance = form.save()
                instance.user = request.user
                instance.is_exam = True
                question_slug = form.cleaned_data['hidden_question']
                question = Question.objects.get(slug=question_slug)
                model_answer = question.model_answer
                response_answer = instance.body
                sentence_embeddings = sbert_model.encode(
                    [model_answer, response_answer])
                score = cosine_similarity(sentence_embeddings)[0][1]
                instance.marks = round(score*100)
                total_marks.append(instance.marks)
                instance.question = question
                instance.save()
                exam_response.responses.add(instance)
                exam_response.marks = round(sum(total_marks)/len(questions))
                exam_response.save()
        return redirect('exam-home')
    else:
        formset = ExamResponseFormset()
    context = {
        'formset': zip(formset, questions),
        'formset2': formset
    }
    return render(request, 'quiz/add_response.html', context=context)
