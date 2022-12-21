from django.shortcuts import render

tAddress = {
    'tIndex': 'web\\index.html',
}

def index(request):
    return render(request, tAddress['tIndex'], {})
