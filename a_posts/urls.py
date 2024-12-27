from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'a_posts'
urlpatterns = [
    path('', views.ViewHome.as_view(), name='home_view'),
    path('tag/<tag>/', views.ViewHome.as_view(), name='posts-by-tag'),
    path('create/', views.ViewCreatePost.as_view(), name='post-create'),
    path('delete/<pk>', views.ViewDeletePost.as_view(), name='post-delete'),
    path('update/<pk>', views.ViewUpdatePost.as_view(), name='post-update'),
    path('post/<pk>', views.ViewPagePost.as_view(), name='post'),
    path('delete-comment/<pk>', views.ViewDeleteComment.as_view(), name='delete-comment'),
]
