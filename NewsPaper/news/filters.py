# импортируем filterset, чем-то напоминающий знакомые дженерики
from django_filters import FilterSet, DateFilter, CharFilter
from django.forms import DateInput

from .models import Post


# создаём фильтр
class PostFilter(FilterSet):
    date = DateFilter(
        field_name='dateCreation',
        label='Дата (позже)',
        lookup_expr='date__gt',
        widget=DateInput(
            attrs={
                'type': 'date',
            }
        ),
    )
    title = CharFilter(
        field_name='title',
        label='Название',
        lookup_expr='icontains',
    )
    author = CharFilter(
        field_name='author__authorUser__username',
        label='Автор',
        lookup_expr='icontains',
    )
    text = CharFilter(
        field_name='text',
        label='По Тексту',
        lookup_expr='icontains',
    )

    class Meta:
        model = Post
        fields = [
            'date',
            'title',
            'author',
            'text',
        ]
