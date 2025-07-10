from django.db import models

from users.models import User


# Create your models here.
class Dictionary(models.Model):
    name = models.CharField(blank=False, null=False)
    source_lang = models.CharField(blank=False, null=False)
    target_lang = models.CharField(blank=False, null=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dictionaries", blank=False, null=False)


class Word(models.Model):
    word = models.CharField(blank=False, null=False)
    translation = models.CharField(blank=False, null=False)

    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE, related_name="words", blank=False, null=False)
