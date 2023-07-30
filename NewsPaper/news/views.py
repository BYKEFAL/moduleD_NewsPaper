from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
# from django.shortcuts import render
# from django.views import View
# from django.core.paginator import Paginator

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
        # context['form'] = PostForm()
        return context

    # def post(self, request, *args, **kwargs):
    #     # создаём новую форму, забиваем в неё данные из POST-запроса
    #     form = self.form_class(request.POST)
    #     if form.is_valid():  # если пользователь ввёл всё правильно и нигде не накосячил, то сохраняем новый товар
    #         form.save()
    #     return super().get(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     # берём значения для нового продукта из POST-запроса, отправленного на сервер
    #     author = request.POST['author']
    #     title = request.POST['title']
    #     type = request.POST['type']
    #     text = request.POST['text']
    #     # создаём новый продукт и сохраняем
    #     user = Author.objects.create(
    #         authorUser=User.objects.create_user(username=author, first_name=author))
    #     post = Post(author=user, title=title,
    #                 categoryType=type, text=text)
    #     post.save()
    #     # отправляем пользователя обратно на GET-запрос
    #     return super().get(request, *args, **kwargs)


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
    template_name = 'news/onepost.html'
    context_object_name = 'onepost'


class PostDetailView(DetailView):
    model = Post
    template_name = 'news/post_detail.html'
    # queryset = Post.objects.all()


class PostCreate(CreateView):
    template_name = 'news/post_create.html'
    form_class = PostForm


class PostUpdate(UpdateView):
    template_name = 'news/post_create.html'
    form_class = PostForm

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


# class Posts(View):

#     def get(self, request):
#         posts = Post.objects.order_by('-id')
#         p = Paginator(posts, 5)
#         posts = p.get_page(request.GET.get('page', 1))
#         data = {
#             'posts': posts,
#         }

#         return render(request, 'news/post_search.html', data)
