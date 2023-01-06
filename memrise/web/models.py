from django.db import models
from django.contrib.auth.models import User

class Deck(models.Model):
    title = models.CharField(max_length=63)
    description = models.CharField(max_length=1023)
    users = models.ManyToManyField(User)
    
    def __str__(self):
        return self.title

class Flashcard(models.Model):
    question = models.CharField(max_length=63)
    answer = models.CharField(max_length=63)
    description = models.CharField(max_length=255)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.question

class Holder(models.Model):
    learned = models.IntegerField(default=0)
    NumOfReviews = models.IntegerField(default=0)
    LastReview = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.flashcard.question + ' for ' + self.user.username

