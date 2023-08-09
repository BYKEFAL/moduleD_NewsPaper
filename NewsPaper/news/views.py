from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, resolve
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views import View
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings
# from django_filters.views import BaseFilterView

from .filters import PostFilter
from .models import *
from .forms import PostForm


class PostList(ListView):
    model = Post
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    ordering = ['-dateCreation']
    paginate_by = 10
    # не знаю почему так, Django ругался, добавил form_class = PostForm, форма заработала.
    # form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['choices'] = Post.CATEGORY_CHOICES
        return context


class PostSearch(ListView):
    model = Post
    template_name = 'news/post_search.html'
    context_object_name = 'posts_search'
    ordering = ['-dateCreation']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(
            self.request.GET, queryset=self.get_queryset())
        return context

# первая detail вьюшка, пока оставлю.


class PostDetail(DetailView):
    model = Post
    template_name = 'news/post_detail_one.html'
    context_object_name = 'onepost'


class PostDetailView(DetailView):
    model = Post
    template_name = 'news/post_detail.html'
    # queryset = Post.objects.all()


class PostCreate(PermissionRequiredMixin, CreateView):
    template_name = 'news/post_create.html'
    form_class = PostForm
    permission_required = ('news.add_post')


class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'news/post_create.html'
    form_class = PostForm
    success_url = reverse_lazy('news:post_search')
    permission_required = ('news.change_post')

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('news:post_search')


class Home(TemplateView):
    template_name = 'homepage/home.html'


class CategoryView(ListView):
    model = Category
    template_name = 'category/category.html'
    context_object_name = 'categories'
    ordering = ['-name']


def CategoryDetail(request, pk):
    category = Category.objects.get(pk=pk)
    is_subscribed = True if len(
        category.subscribers.filter(id=request.user.id)) else False

    return render(
        request,
        'category/category_detail.html',
        {
            'category': category,
            'is_subscribed': is_subscribed,
            'subscribers': category.subscribers.all()
        }
    )


@login_required
def CategorySubscribe(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)

    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user)
        # email = user.email
        html = render_to_string(
            'mailing/notification_subscribe.html',
            {
                'category': category,
                'user': user,
            },
        )

        msg = EmailMultiAlternatives(
            subject=f'Подтверждение подписи на категорию - {category.name}',
            body='спасибо что подписались!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            # это то же, что и recipients_list - передаем коллекцию
            to=[settings.MY_TEST_EMAIL, ],
        )

        msg.attach_alternative(html, 'text/html')
        try:
            msg.send()  # отсылаем
        except Exception as e:
            print(e)
        redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def CategoryUnsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)

    if category.subscribers.filter(id=user.id).exists():
        category.subscribers.remove(request.user.id)

    return redirect(request.META.get('HTTP_REFERER'))
