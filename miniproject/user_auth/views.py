from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse
from quiz.models import Question, Response, Exam, ExamResponse
from .models import User
from django.views.generic import UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth import logout
# Create your views here.


def Home(request):
    return render(request, "custom/home.html")


@login_required
def dashboard(request):
    user = request.user
    questions_created = Question.objects.filter(
        author=user, is_exam=False).order_by("-date_added")
    questions_responded = Response.objects.filter(
        user=user, is_exam=False).order_by("-date_added")
    exams_created = Exam.objects.filter(author=user).order_by("-date_added")
    exams_answered = ExamResponse.objects.filter(
        user=user).order_by("-date_added")
    context = {
        'questions': questions_created,
        'responses': questions_responded,
        'exams': exams_created,
        'exam_response': exams_answered
    }
    return render(request, 'custom/dashboard.html', context=context)


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name']
    template_name = 'custom/user_update.html'

    def get_success_url(self):
        return reverse('dashboard')

    def test_func(self):
        if self.request.user == self.get_object():
            return True
        return False


def logout_user(request):
    logout(request)
    return redirect('home')
