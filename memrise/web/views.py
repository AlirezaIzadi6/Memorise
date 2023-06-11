'''
functions to manage contents that will be sent to urls will be put here.
'''
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import Deck, Flashcard, Holder

tAddress = {
    'tIndex': 'web\\index.html',
    'tShowdecks': 'web\\decks-show.html',
    'tShowmydecks': 'web\\my-decks-show.html',
    'tError_login': 'web\\error-login.html',
    'tShowdeck': 'web\\deck-show.html',
    'tAddbatchflashcard': 'web\\flashcard-add.html',
}

def index(request):
    '''
    simply return the index page.
    '''
    context = {'messages': request.session.get('messages')}
    request.session['messages'] = []
    return render(request, tAddress['tIndex'], context)

def showdecks(request):
    '''
    return all decks in the database in a page.
    '''
    decks = Deck.objects.all()
    num_of_decks = len(decks)
    context = {'decks': decks, 'NumOfDecks': num_of_decks,
        'messages': request.session.get('messages')}
    return render(request, tAddress['tShowdecks'], context)

def showmydecks(request):
    '''
    return only the decks that current user has picked up. else return error_login page.
    '''
    if not request.user.is_authenticated:
        return render(request, tAddress['tError_login'], {})
    decks = Deck.objects.filter(users=request.user)
    context = {'decks': decks, 'messages': request.session.get('messages')}
    request.session['messages'] = []
    return render(request, tAddress['tShowmydecks'], context)

def pickdeck(request, d_id):
    deck = Deck.objects.get(id=d_id)
    user = request.user
    if not user.is_authenticated:
        return render(request, tAddress['tError_login'], {})
    if len(Deck.objects.filter(users=user)) == 0:
        deck.users.add(user)
        cards = Flashcard.objects.filter(deck=deck)
        for card in cards:
            holder = Holder(flashcard=card, user=user)
            holder.save()
        request.session['messages'] = ['با موفقیت به مجموعه های شما اضافه شد.']
    return HttpResponseRedirect(reverse('showdeck', args=(d_id,)))

def quitdeck(request, d_id):
    deck = Deck.objects.get(id=d_id)
    user = request.user
    if len(Deck.objects.filter(users=user)) > 0:
        deck.users.remove(user)
        request.session['messages'] = ['با موفقیت از لیست مجموعه های شما پاک شد.']
    return HttpResponseRedirect(reverse('showdeck', args=(d_id,)))

def showdeck(request, d_id):
    deck = Deck.objects.get(id=d_id)
    cards = Flashcard.objects.filter(deck=deck)
    registered = False
    if request.user.is_authenticated and len(Deck.objects.filter(users=request.user)):
        registered = True
    context = {'deck': deck, 'cards': cards,
        'registered': registered, 'messages': request.session.get('messages')}
    request.session['messages'] = []
    return render(request, tAddress['tShowdeck'], context)

def addbatchflashcard(request, d_id):
    deck = Deck.objects.get(id=d_id)
    context = {'deck': deck, 'messages': request.session.get('messages')}
    request.session['messages'] = []
    return render(request, tAddress['tAddbatchflashcard'], context)

def submitbatchflashcard(request, d_id):
    deck = Deck.objects.get(id=d_id)
    lines = request.POST['data'].split('\n')
    counter = 0
    for line in lines:
        parsed = line.split('^^') if len(line.split('^^')) > 1 else line.split('\t')
        if len(parsed) < 2:
            continue
        card = Flashcard(deck=deck, question=parsed[0], answer=parsed[1])
        if len(parsed) > 2:
            card.description = parsed[2]
        card.save()
        counter += 1
    if request.POST['data'] == '':
        request.session['messages'] = [
            'ورودی از سمت شما ارسال نشده و هیچ کارتی به مجموعه اضافه نشد.']
    elif counter == 0:
        request.session['messages'] = [
            'هیچ کارتی به مجموعه اضافه نشد. بعد از چک کردن ورودی دوباره تلاش کنید.']
    else:
        request.session['messages'] = [
            'از ' + str(len(lines)) +
            ' ورودی ارسال شده ' + str(counter) +
            ' کارت با موفقیت اضافه شد.']
    return HttpResponseRedirect(reverse('showdeck', args=(deck.id,)))
