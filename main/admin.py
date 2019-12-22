from django.contrib import admin

from .models import Account, SearchWord, ScoreWord

admin.site.register(Account)
admin.site.register(SearchWord)
admin.site.register(ScoreWord)
