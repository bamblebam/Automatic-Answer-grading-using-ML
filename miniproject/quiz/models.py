from django.db import models
from user_auth.models import User
from django.template.defaultfilters import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from uuid import uuid4
# Create your models here.


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    model_answer = models.TextField(null=True)
    question_code = models.CharField(max_length=200, default=uuid4().hex[:6])
    slug = models.SlugField(max_length=255, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_exam = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(uuid4().hex[:10])
        super(Question, self).save(*args, **kwargs)


class Response(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='responses')
    body = models.TextField(null=False)
    marks = models.IntegerField(default=0, validators=[
                                MinValueValidator(0), MaxValueValidator(100)])
    slug = models.SlugField(max_length=255, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_exam = models.BooleanField(default=False)

    def __str__(self):
        return self.body

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(uuid4().hex[:10])
        super(Response, self).save(*args, **kwargs)


class Exam(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    num_questions = models.IntegerField(default=5, validators=[
        MinValueValidator(1), MaxValueValidator(100)])
    questions = models.ManyToManyField(Question, symmetrical=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    exam_code = models.CharField(
        max_length=200, default=uuid4().hex[:6], null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(uuid4().hex[:10])
        super(Exam, self).save(*args, **kwargs)


class ExamResponse(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, null=True, blank=True)
    responses = models.ManyToManyField(Response, symmetrical=False)
    slug = models.SlugField(max_length=200, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    marks = models.IntegerField(default=0, validators=[
        MinValueValidator(1), MaxValueValidator(100)])

    def __str__(self):
        return self.exam.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(uuid4().hex[:10])
        super(ExamResponse, self).save(*args, **kwargs)
