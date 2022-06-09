from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

from base.models import AboutPage, Comment, HomePageBlock, Post, Newsletter


def home(request):
    homepage_block = HomePageBlock.objects.first()
    featured_post_list = Post.objects.filter(featured=True).order_by('-id')[:3]
    latest_post_list = Post.objects.order_by('-id')[:3]

    if request.method == 'POST':
        new_email = request.POST.get('email')
        newsletter = Newsletter(email=new_email)
        newsletter.save()

    context = {
        'featured_post_list': featured_post_list,
        'latest_post_list': latest_post_list,
        'homepage_block': homepage_block
    }
    return render(request, 'home.html', context)


def about(request):
    about_page = AboutPage.objects.first()
    return render(request, 'about.html', {'about': about_page})


def post_list(request):
    posts = Post.objects.all().order_by('-id')

    # pagination
    paginator = Paginator(posts, 4)
    page_request_variable = 'page'
    page_number = request.GET.get(page_request_variable)
    try:
        paginated_posts = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_posts = paginator.page(1)
    except EmptyPage:
        paginated_posts = paginator.page(paginator.num_pages)

    context = {
        'post_list': paginated_posts,
        'page_request_variable': page_request_variable,
    }
    return render(request, 'posts.html', context)


def post_detail(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        content = request.POST.get('content')
        comment = Comment(name=name, email=email, content=content, post=post)
        comment.save()
    context = {
        'post': post,
        }
    return render(request, 'post.html', context)


def blog_search(request):
    q = request.GET.get('q')
    search_result = None
    if q:
        post_queryset = Post.objects.all()
        search_result = post_queryset.filter(
            Q(title__icontains=q) |
            Q(overview__icontains=q)
        ).distinct()
    return render(request, 'search.html', {'posts': search_result})


def tag(request, title):
    posts = Post.objects.filter(tags__title=title)
    return render(request, 'search.html', {'posts': posts})


def category(request, title):
    posts = Post.objects.filter(categories__title=title)
    return render(request, 'search.html', {'posts': posts})
