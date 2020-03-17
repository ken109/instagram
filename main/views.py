from datetime import datetime

from django.shortcuts import render, redirect

from instagram.settings import TITLE

from .models import Account, SearchWord
from .forms import TagsForm


def invisible(request, id):
    account = Account.objects.get(id=id)
    account.invisible = 1
    account.save()
    return redirect('index')


def delete_tag(request, id):
    SearchWord.objects.get(id=id).delete()
    return redirect('tag')


def add_tag(request):
    form = TagsForm(request.POST or None)
    if form.is_valid():
        SearchWord.objects.update_or_create(
            word=form.cleaned_data['word'],
            defaults={
                'score': form.cleaned_data['score'],
            }
        )
        return redirect('tag')
    return render(request, 'main/edit_tag.html', {'title': TITLE, 'form': form})


def account(request):
    accounts = Account.objects.filter(invisible=0).order_by('-score').all()[:99]
    scoring = Account.objects.order_by('-scored_at').first()
    return render(request, 'main/accounts.html', {'title': TITLE, 'accounts': accounts, 'scoring': scoring})


def tag(request):
    tags = SearchWord.objects.order_by('-score').all()[:100]
    searching = SearchWord.objects.order_by('-searched_at').first()
    scoring = SearchWord.objects.order_by('-scored_at').first()
    today_accounts = Account.objects.filter(created_at__gte=datetime.now().date())
    today_tags = SearchWord.objects.filter(created_at__gte=datetime.now().date())
    return render(request, 'main/tags.html',
                  {'title': TITLE, 'tags': tags, 'searching': searching, 'scoring': scoring,  'today_accounts': len(today_accounts),
                   'today_tags': len(today_tags)})
