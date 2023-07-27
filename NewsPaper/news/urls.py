from django.urls import path
from .views import PostDetail, PostList, PostSearch

urlpatterns = [
    path('', PostList.as_view()),
    path('search/', PostSearch.as_view()),
    path('<int:pk>', PostDetail.as_view()),

]
