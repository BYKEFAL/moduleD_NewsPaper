from django.views.generic import ListView, DetailView, TemplateView
from .models import Post


class PostList(ListView):
    model = Post
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')


class PostDetail(DetailView):
    model = Post
    template_name = 'news/onepost.html'
    context_object_name = 'onepost'


class Home(TemplateView):
    template_name = 'homepage/home.html'
