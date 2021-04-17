from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from .models import Response, ExamResponse, Question, Exam
from user_auth.models import User


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


def details_filled(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.first_name and user.last_name and user.roll_no:
            messages.warning(request,
                             "Fill in your details before proceeding.", extra_tags='details')
            return function(request, *args, **kwargs)
        return redirect('user-update', user.slug)
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


class DetailsFilledMixin():
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.first_name and user.last_name and user.roll_no:
            messages.warning(request,
                             "Fill in your details before proceeding.", extra_tags='details')
            return super().dispatch(request, *args, **kwargs)
        return redirect('user-update', user.slug)
