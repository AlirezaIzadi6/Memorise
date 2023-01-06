from django.shortcuts import render

tAddress = {
    'tIndex': 'web\\index.html',
}

def index(request):
    user = request.user
    context = {'user': user}
    return render(request, tAddress['tIndex'], context)
