from django.views.generic import ListView, DetailView, TemplateView
# from django.shortcuts import render
# from django.views import View
# from django.core.paginator import Paginator

from .filters import PostFilter
from .models import Post


class PostList(ListView):
    model = Post
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    ordering = ['-dateCreation']
    paginate_by = 10


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


class PostDetail(DetailView):
    model = Post
    template_name = 'news/onepost.html'
    context_object_name = 'onepost'


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
