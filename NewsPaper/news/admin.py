from django.contrib import admin
from .models import *


# все аргументы уже должны быть вам знакомы, самые нужные из них это request — объект хранящий информацию о запросе и queryset — грубо говоря набор объектов, которых мы выделили галочками.
def nullfy_rating(modeladmin, request, queryset):
    queryset.update(rating=0)


def nullfy_rating_author(modeladmin, request, queryset):
    queryset.update(ratingAuthor=0)


nullfy_rating.short_description = 'Обнулить рейтинг выбранных новостей'
nullfy_rating_author.short_description = 'Обнулить рейтинг авторов'


class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    # генерируем список имён всех полей для более красивого отображения
    list_display = ['title', 'author', 'categoryType',
                    'dateCreation',  'preview', 'rating']
    # добавляем примитивные фильтры в нашу админку
    list_filter = ('author', 'rating', 'postCategory')
    search_fields = ('title', 'text')
    actions = [nullfy_rating]  # добавляем действия в список


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['authorUser', 'ratingAuthor']
    search_fields = ('authorUser__username', 'ratingAuthor')
    actions = [nullfy_rating_author]


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name', 'subscribers__username')


admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
