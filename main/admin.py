from django.contrib import admin

from .models import ScoreWord, ScoreWordAdmin

admin.site.register(ScoreWord, ScoreWordAdmin)
