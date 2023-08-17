from django.urls import path
from .views import PostDetail, PostList, PostSearch, PostDetailView, PostCreate, PostUpdate, PostDelete
from .views import CategoryView, CategoryDetail, CategorySubscribe, CategoryUnsubscribe
from django.views.decorators.cache import cache_page

app_name = 'news'
urlpatterns = [
    path('', cache_page(60)(PostList.as_view()), name='news'),
    path('search/', PostSearch.as_view(), name='post_search'),
    #     path('<int:pk>/', cache_page(300)
    #          (PostDetail.as_view()), name='first_post_detail'),
    #     path('detail/<int:pk>/', cache_page(300)(PostDetailView.as_view()),
    #          name='second_post_detail'),
    path('<int:pk>/', PostDetail.as_view(), name='first_post_detail'),
    path('detail/<int:pk>/', PostDetailView.as_view(), name='second_post_detail'),
    path('add/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('category/', CategoryView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetail, name='category_detail'),
    path('category/<int:pk>/subcribe/',
         CategorySubscribe, name='category_subscribe'),
    path('category/<int:pk>/unsubcribe/',
         CategoryUnsubscribe, name='category_unsubscribe'),
]
