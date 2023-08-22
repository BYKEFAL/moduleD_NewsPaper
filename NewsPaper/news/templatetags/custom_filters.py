from django import template
from better_profanity import profanity

register = template.Library()

# Чтобы не забыть почитать про декораторами simple_tag и inclusion_tag
# @register.simple_tag
# def current_time(format_string):
#     return datetime.datetime.now().strftime(format_string)


@register.filter(name='censor')
def censor(value):
    custom_badwords = ['нехорошие слова']
    # Можно добавить своих плохих слов
    profanity.add_censor_words(custom_badwords)
    censored = profanity.censor(value, '*$')
    return censored
