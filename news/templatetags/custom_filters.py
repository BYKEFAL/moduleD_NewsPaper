from django import template
from better_profanity import profanity

register = template.Library()


@register.filter(name='censor')
def censor(value):
    custom_badwords = ['нехорошие слова']
    # Можно добавить своих плохих слов
    profanity.add_censor_words(custom_badwords)
    censored = profanity.censor(value, '*$')
    return censored
