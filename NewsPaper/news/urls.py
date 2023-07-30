from django.urls import path
from .views import PostDetail, PostList, PostSearch, PostDetailView, PostCreate, PostUpdate, PostDelete

app_name = 'news'
urlpatterns = [
    path('', PostList.as_view(), name='news'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('<int:pk>', PostDetail.as_view(), name='first_post_detail'),
    # немного разные Detail, пока оставил потом отредактирую
    path('detail/<int:pk>', PostDetailView.as_view(), name='second_post_detail'),
    path('add/', PostCreate.as_view(), name='post_create'),
    # делаю как требуют по тех. заданию, у меня пути по другому.
    path('<int:pk>/edit', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
]
