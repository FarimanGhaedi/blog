from django.urls import path

from base import views


urlpatterns = [
    path('', views.home, name="home"),
    path('about', views.about , name="about"),
    path('blog/search', views.blog_search, name='blog_search'),
    path('blog/archive', views.post_list, name="blog_archive"),
    path('blog/article/<int:id>', views.post_detail, name="blog_article"),
    path('blog/categories/<str:title>', views.category, name='category_articles'),
    path('blog/tags/<str:title>', views.tag, name='tag_articles')
]
