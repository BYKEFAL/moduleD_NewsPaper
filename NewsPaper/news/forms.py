from django.forms import ModelForm
from .models import *
from django import forms

# Создаём модельную форму


class PostForm(ModelForm):
    # В класс мета, как обычно, надо написать модель, по которой будет строиться форма, и нужные нам поля. Мы уже делали что-то похожее с фильтрами

    class Meta:
        model = Post
        author = User
        fields = ['author', 'title', 'categoryType', 'postCategory', 'text']
        widgets = {
            'author': forms.Select(attrs={'class': 'form-control', }),
            'title': forms.TextInput(attrs={'class': 'form-control', }),
            'categoryType': forms.Select(attrs={'class': 'form-control', }),
            'postCategory': forms.CheckboxSelectMultiple(),
            'text': forms.Textarea(attrs={'class': 'form-control', }),
        }
        labels = {
            'categoryType': 'Type',
            'postCategory': 'Category'
        }
