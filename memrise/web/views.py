from django.shortcuts import render

from .models import *

tAddress = {
    'tIndex': 'web\\index.html',
    'tShowdecks': 'web\\showdecks.html',
    'tError_login': 'web\\error_login.html',
}

def index(request):
    user = request.user
    context = {'user': user}
    return render(request, tAddress['tIndex'], context)

def showdecks(request):
    if request.user.is_authenticated:
        decks = Deck.objects.filter(users=request.user)
        context = {'decks': decks}
        return render(request, tAddress['tShowdecks'], context)
    else:
        return render(request, tAddress['tError_login'], {})