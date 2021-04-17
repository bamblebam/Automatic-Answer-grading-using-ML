from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from uuid import uuid4

# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    roll_no = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, unique=True)
    email = models.CharField(max_length=200, unique=True)
    slug = models.SlugField()
    is_teacher = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(uuid4().hex[:10])
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.first_name)+" "+str(self.last_name)
