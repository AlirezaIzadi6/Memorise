from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    
    def getNumOfCardsToReview(self, user):
        holders = Holder.objects.filter(flashcard__deck=self, user=user, learned=2)
        for h in holders:
            h.update()
        return len(Holder.objects.filter(flashcard__deck=self, user=user, NeedToReview=True))
    
    def makeLearnQuestions(self, user):
        l0holders = Holder.objects.filter(flashcard__deck=self, user=user, learned=0)
        l1holders = Holder.objects.filter(flashcard__deck=self, user=user, learned=1)
        if len(l1holders) >= 5:
            cards = l1holders[:5]
        elif len(l0holders) >= 5:
            cards = l1holders[:] + l0holders[:5-len(l1holders)]
        else:
            cards = l1holders[:] + l0holders[:]
        questions = []
        for c in cards:
            if c.learned == 1:
                questions.append(c.flashcard.makeQuestion(2))
                questions.append(c.flashcard.makeQuestion(3))
                questions.append(c.flashcard.makeQuestion(3))
            else:
                questions.append(c.flashcard.makeQuestion(0))
                questions.append(c.flashcard.makeQuestion(1))
                questions.append(c.flashcard.makeQuestion(2))
                questions.append(c.flashcard.makeQuestion(2))
        return questions

class Flashcard(models.Model):
    question = models.CharField(max_length=63)
    answer = models.CharField(max_length=63)
    description = models.CharField(max_length=255, default='', blank=True)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.question
    
    def makeQuestion(self, qtype): # qtype = question type (multiple choice, typing, etc)
        result = {}
        if qtype == 0:
            result = {'question': self.question, 'answer': self.answer, 'description': self.description, 'type': 'learn'}
        elif qtype == 1:
            result = {'question': self.question, 'answer': self.answer, 'type': 'QToA'}
        elif qtype == 2:
            result = {'question': self.answer, 'answer': self.question, 'type': 'AToQ'}
        elif qtype == 3:
            result = {'question': self.question, 'answer': self.answer, 'type': 'Writing'}
        return result

class Holder(models.Model):
    learned = models.IntegerField(default=0)
    NumOfReviews = models.IntegerField(default=0)
    LastReview = models.DateTimeField(null=True, blank=True)
    TimeToReview = models.DateTimeField(null=True, blank=True)
    NeedToReview = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.flashcard.question + ' for ' + self.user.username
    
    def update(self):
        self.NeedToReview = True if timezone.now() > self.TimeToReview else False
        self.save()
