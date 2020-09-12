from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
from PIL import Image
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField(validators=[MinLengthValidator(1, "Your message is empty.")])
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(blank=True, upload_to="images")
    tags = models.ManyToManyField('Tag', through="Tagging")

    def __str__(self):
        return self.title


class Tag(models.Model):
    tag = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tag


class Tagging(models.Model):
    posts = models.ForeignKey('Post', on_delete=models.CASCADE)
    taggings = models.ForeignKey('Tag', on_delete=models.CASCADE)
