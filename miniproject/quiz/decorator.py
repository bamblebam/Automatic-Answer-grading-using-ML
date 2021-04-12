from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from .models import Response, ExamResponse, Question, Exam


def is_teacher(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_teacher:
            return function(request, *args, **kwargs)
        raise PermissionDenied
    return wrap


def question_answered(function):
    @wraps(function)
    def wrap(request, slug, *args, **kwargs):
        response = Question.objects.get(
            slug=slug).responses.filter(user=request.user)
        if len(response) > 0:
            return redirect('already-answered')
        else:
            return function(request, slug, *args, **kwargs)
    return wrap


class IsTeacherMixin():
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_teacher:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied


class ExamAnsweredMixin():
    def dispatch(self, request, *args, **kwargs):
        if ExamResponse.objects.filter(exam=Exam.objects.get(
                slug=self.kwargs.get('slug')), user=self.request.user).exists():
            return redirect('already-answered')
        return super().dispatch(request, *args, **kwargs)
