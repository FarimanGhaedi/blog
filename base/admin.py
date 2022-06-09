from django.contrib import admin

from base.models import AboutPage, Author, Category, Comment, Footer, HomePageBlock, Post, Newsletter, Tag


class HomePageBlockAdmin(admin.ModelAdmin):

    #    def has_add_permission(self, request):
    #        return False

    def has_delete_permission(self, request, obj=None):
        return False


class AboutPageAdmin(admin.ModelAdmin):
    #    def has_add_permission(self, request):
    #        return False

    def has_delete_permission(self, request, obj=None):
        return False


class FooterAdmin(admin.ModelAdmin):

    #    def has_add_permission(self, request):
    #        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Author)
admin.site.register(AboutPage, AboutPageAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Footer, FooterAdmin)
admin.site.register(HomePageBlock, HomePageBlockAdmin)
admin.site.register(Post)
admin.site.register(Newsletter)
admin.site.register(Tag)
