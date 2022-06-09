from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from tinymce.models import HTMLField

User = get_user_model()


class Author(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='author_images', null=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_articles', kwargs={
            'title': self.title
        })


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag_articles', kwargs={
            'title': self.title
        })


class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    content = HTMLField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    comment_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=1)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='thumbnail', null=True)
    categories = models.ManyToManyField(to=Category)
    tags = models.ManyToManyField(to=Tag)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return "title: {} - timestamp: {}".format(self.title, self.timestamp)

    def get_absolute_url(self):
        return reverse('blog_article', kwargs={
            'id': self.id
        })

    def get_previous_post(self):
        previous_post = Post.objects.filter(id__lt=self.id).order_by('id').last()
        if previous_post:
            previous_url = reverse('blog_article', kwargs={'id': previous_post.id})
            previous_title = previous_post.title
        else:
            previous_url = None
            previous_title = ''
        return {'url': previous_url, 'title': previous_title}

    def get_next_post(self):
        next_post = Post.objects.filter(id__gt=self.id).order_by('id').first()
        if next_post:
            next_url = reverse('blog_article', kwargs={'id': next_post.id})
            next_title = next_post.title
        else:
            next_url = None
            next_title = None
        return {'url': next_url, 'title': next_title}


class Comment(models.Model):
    name = models.CharField(max_length=50, default='Anonymous')
    email = models.EmailField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='post_comments')

    def __str__(self):
        return "{} - {}".format(self.name, self.post.title)


class Newsletter(models.Model):
    email = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.email, self.timestamp)


class HomePageBlock(models.Model):
    # Hero Section
    hero_background_image = models.ImageField(upload_to='homepage', null=True)
    hero_content = HTMLField(default="Django Blog - A Free Django Template")
    # Intro Section
    intro_content = HTMLField(default="Place a nice introduction here to catch reader's attention. Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderi.")
    # Divider Section
    divider_content = HTMLField(default="Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua")
    divider_background_image = models.ImageField(upload_to='homepage', null=True)
    # Latest Posts
    latest_posts_content = HTMLField(default="Latest Post")
    # Newsletter
    newsletter_content = HTMLField(default="<h2>Subscribe to Newsletter</h2></br>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")

    def __str__(self):
        return "homepage blocks"

    def save(self, *args, **kwargs):
        if not self.pk and HomePageBlock.objects.exists():
            raise ValidationError("You can create only one HomePageBlock instance")
        return super(HomePageBlock, self).save(*args, **kwargs)


class AboutPage(models.Model):
    # Hero Section
    hero_background_image = models.ImageField(upload_to='homepage', null=True)
    hero_content = HTMLField(default="Django Blog - A Free Django Template")
    # Main Section
    main_content = HTMLField(default="Place a nice introduction here to catch reader's attention. Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderi.")
    # Google Map
    map = HTMLField(null=True, blank=True)

    def __str__(self):
        return "about page blocks"

    def save(self, *args, **kwargs):
        if not self.pk and AboutPage.objects.exists():
            raise ValidationError("You can create only one AboutPage instance")
        return super(AboutPage, self).save(*args, **kwargs)


class Footer(models.Model):
    copyright_content = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    social_media_1_font_code = models.CharField(max_length=20, null=True, blank=True)
    social_media_1_link = models.CharField(max_length=50, null=True, blank=True)
    social_media_2_font_code = models.CharField(max_length=20, null=True, blank=True)
    social_media_2_link = models.CharField(max_length=50, null=True, blank=True)
    social_media_3_font_code = models.CharField(max_length=20, null=True, blank=True)
    social_media_3_link = models.CharField(max_length=50, null=True, blank=True)
    social_media_4_font_code = models.CharField(max_length=20, null=True, blank=True)
    social_media_4_link = models.CharField(max_length=50, null=True, blank=True)
    social_media_5_font_code = models.CharField(max_length=20, null=True, blank=True)
    social_media_5_link = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return "footer blocks"

    def save(self, *args, **kwargs):
        if not self.pk and Footer.objects.exists():
            raise ValidationError("You can create only one Footer instance")
        return super(Footer, self).save(*args, **kwargs)
