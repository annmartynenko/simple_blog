"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, reverse_lazy
from blog import views

app_name='blog'
urlpatterns = [
    path('', views.PostListView.as_view()),
    path('posts', views.PostListView.as_view(), name='all'),
    path('posts/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/create',
         views.PostCreateView.as_view(success_url=reverse_lazy('blog:all')), name='post_create'),
    path('posts/<int:pk>/update',
         views.PostUpdateView.as_view(success_url=reverse_lazy('blog:all')), name='post_update'),
    path('posts/<int:pk>/delete',
         views.PostDeleteView.as_view(success_url=reverse_lazy('blog:all')), name='post_delete'),
    path('registration', views.RegistrationView.as_view(), name='registration'),
    path('tag/<int:pk>', views.TagDetailView.as_view(), name='tag'),
    path('tag/create',
         views.TagCreateView.as_view(success_url=reverse_lazy('blog:all')), name='tag_create'),
    path('post/<int:pk>/connect',
         views.PostConnectView.as_view(success_url=reverse_lazy('blog:all')), name='post_connect'),

]
