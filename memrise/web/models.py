from django.db import models
from django.contrib.auth.models import User

class Deck(models.Model):
    title = models.CharField(max_length=63)
    description = models.CharField(max_length=1023, null=True, blank=True)
    users = models.ManyToManyField(User, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def getNumOfCards(self):
        return len(Flashcard.objects.filter(deck=self))
    
    def getNumOfLearners(self):
        return len(User.objects.filter(deck=self))

class Flashcard(models.Model):
    question = models.CharField(max_length=63)
    answer = models.CharField(max_length=63)
    description = models.CharField(max_length=255, null=True, blank=True)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.question

class Holder(models.Model):
    learned = models.IntegerField(default=0)
    NumOfReviews = models.IntegerField(default=0)
    LastReview = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.flashcard.question + ' for ' + self.user.username

