"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from blog.apps import BlogConfig
from django.views.decorators.cache import cache_page, never_cache
from blog.views import (MainListView, BlogListView, BlogCreateView, BlogDetailView,
                        BlogUpdateView, BlogDeleteView,)


app_name = BlogConfig.name


urlpatterns = [
    path('', never_cache(MainListView.as_view()), name='main'),

    path('blog/', cache_page(60)(BlogListView.as_view()), name='blog_list'),
    path('blog/create/', never_cache(BlogCreateView.as_view()), name='blog_create'),
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/edit/<slug:slug>/', never_cache(BlogUpdateView.as_view()), name='blog_update'),
    path('blog/delete/<slug:slug>/', BlogDeleteView.as_view(), name='blog_delete'),
]
