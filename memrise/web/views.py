from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import *

messages = []
tAddress = {
    'tIndex': 'web\\index.html',
    'tShowdecks': 'web\\show-decks.html',
    'tError_login': 'web\\error-login.html',
    'tShowdeck': 'web\\deck-show.html',
    'tAddbatchflashcard': 'web\\flashcard-add.html',
}

def index(request):
    global messages
    user = request.user
    context = {'user': user, 'messages': messages}
    messages = []
    return render(request, tAddress['tIndex'], context)

def showdecks(request):
    global messages
    if request.user.is_authenticated:
        decks = Deck.objects.filter(users=request.user)
        context = {'decks': decks, 'messages': messages}
        messages = []
        return render(request, tAddress['tShowdecks'], context)
    else:
        return render(request, tAddress['tError_login'], {})

def showdeck(request, d_id):
    global messages
    deck = Deck.objects.get(id=d_id)
    cards = Flashcard.objects.filter(deck=deck)
    context = {'deck': deck, 'cards': cards, 'messages': messages}
    messages = []
    return render(request, tAddress['tShowdeck'], context)

def addbatchflashcard(request, d_id):
    global messages
    deck = Deck.objects.get(id=d_id)
    context = {'deck': deck, 'messages': messages}
    messages = []
    return render(request, tAddress['tAddbatchflashcard'], context)

def submitbatchflashcard(request, d_id):
    global messages
    deck = Deck.objects.get(id=d_id)
    data = request.POST['data'].split('\n')
    counter = 0
    for d in data:
        parsed = d.split(',')
        if len(parsed) < 3:
            continue
        card = Flashcard(deck=deck, question=parsed[0], answer=parsed[1], description=parsed[2])
        card.save()
        counter += 1
    if request.POST['data'] == '':
        messages.append('ورودی از سمت شما ارسال نشده و هیچ کارتی به مجموعه اضافه نشد.')
    elif counter == 0:
        messages.append('هیچ کارتی به مجموعه اضافه نشد. بعد از چک کردن ورودی دوباره تلاش کنید.')
    else:
        messages.append('از ' + str(len(data)) + ' ورودی ارسال شده ' + str(counter) + ' کارت با موفقیت اضافه شد.')
    return HttpResponseRedirect(reverse('showdeck', args=(deck.id,)))
