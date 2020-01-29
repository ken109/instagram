from django.shortcuts import render, redirect

from .models import Account, SearchWord


def invisible(request, id):
    account = Account.objects.get(id=id)
    account.invisible = 1
    account.save()
    return redirect('index')


def delete_tag(request, id):
    SearchWord.objects.get(id=id).delete()
    return redirect('tag')


def mam(request):
    accounts = Account.objects.filter(invisible=0).order_by('-score').all()[:99]
    return render(request, 'main/score.html', {'accounts': accounts})


def tag(request):
    tags = SearchWord.objects.order_by('-score').all()[:100]
    return render(request, 'main/tags.html', {'tags': tags})
