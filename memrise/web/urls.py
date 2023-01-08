from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('decks', views.showdecks, name='showdecks'),
    path('mydecks', views.showmydecks, name='showmydecks'),
    path('deck/<int:d_id>/add', views.pickdeck, name='pickdeck'),
    path('deck/<int:d_id>/quit', views.quitdeck, name='quitdeck'),
    path('deck/<int:d_id>/addbatchflashcard', views.addbatchflashcard, name='addbatchflashcard'),
    path('deck/<int:d_id>/submitbatchflashcard', views.submitbatchflashcard, name='submitbatchflashcard'),
    path('deck/<int:d_id>', views.showdeck, name='showdeck'),
]
