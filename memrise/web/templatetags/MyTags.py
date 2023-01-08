from django import template
register = template.Library()

@register.filter
def getNumOfCardsToReview(d, user):
    return d.getNumOfCardsToReview(user)
