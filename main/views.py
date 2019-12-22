from django.shortcuts import render, redirect

from .models import Account


def index(request):
    accounts = Account.objects.filter(invisible=0).order_by('-score').all()[:100]
    return render(request, 'main/score.html', {'accounts': accounts})


def invisible(request, id):
    account = Account.objects.get(id=id)
    account.delete()
    return redirect('index')
