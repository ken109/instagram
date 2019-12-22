from django.db import models


class Account(models.Model):
    url = models.CharField(max_length=255, unique=True)
    score = models.IntegerField(default=0)
    name = models.CharField(max_length=255)
    img = models.CharField(max_length=255)
    followed = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SearchWord(models.Model):
    word = models.CharField(max_length=63, unique=True)
    searched_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.word


class ScoreWord(models.Model):
    word = models.CharField(max_length=63, unique=True)
    score = models.IntegerField(default=1)

    def __str__(self):
        return self.word
