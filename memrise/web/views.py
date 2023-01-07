from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import *

tAddress = {
    'tIndex': 'web\\index.html',
    'tShowdecks': 'web\\showdecks.html',
    'tError_login': 'web\\error_login.html',
    'tShowdeck': 'web\\showdeck.html',
    'tAddbatchflashcard': 'web\\addbatchflashcard.html',
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

def showdeck(request, d_id):
    deck = Deck.objects.get(id=d_id)
    cards = Flashcard.objects.filter(deck=deck)
    context = {'deck': deck, 'cards': cards}
    return render(request, tAddress['tShowdeck'], context)

def addbatchflashcard(request, d_id):
    deck = Deck.objects.get(id=d_id)
    context = {'deck': deck}
    return render(request, tAddress['tAddbatchflashcard'], context)

def submitbatchflashcard(request, d_id):
    deck = Deck.objects.get(id=d_id)
    data = request.POST['data']
    for d in data.split('\n'):
        parsed = d.split(',')
        if len(parsed) < 3:
            continue
        card = Flashcard(deck=deck, question=parsed[0], answer=parsed[1], description=parsed[2])
        card.save()
    return HttpResponseRedirect(reverse('showdeck', args=(deck.id,)))
