import datetime
from django.db.models import Count

from base.models import Footer, Post, Tag, Category


def get_category_count():
    queryset = Post.objects.values('categories__title').annotate(Count('categories'))
    for item in queryset:
        cat = Category.objects.filter(title=item['categories__title']).first()
        item['url'] = cat.get_absolute_url
    return queryset


def footer(request):
    current_datetime = datetime.datetime.now()
    footer_items = Footer.objects.first()
    return {
        'footer_current_year': current_datetime.year,
        'footer_items': footer_items
    }


def sidebar(request):
    posts = Post.objects.all().order_by('-id')[:3]
    tags = Tag.objects.order_by('title')
    return {
        'sidebar_recent_posts': posts,
        'sidebar_tags': tags,
        'sidebar_categories': get_category_count(),
    }
