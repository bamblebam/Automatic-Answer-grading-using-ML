from logging import disable

from django.db.models import fields
from .models import Question, Response
from django import forms


class NewQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'model_answer']
        widgets = {
            'title': forms.TextInput(attrs={
                'autofocus': True,
                'placeholder': 'How to create a Q&A website with Django?'
            })
        }


class NewResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['body']


class ResponseUpdateForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea, disabled=True)
    marks = forms.IntegerField(min_value=0, max_value=100)

    class Meta:
        model = Response
        fields = ['body', 'marks']
