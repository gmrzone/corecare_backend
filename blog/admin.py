from django.contrib import admin
from .models import Post, Comment, PostImage


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','author', 'active')
    list_editable = ('active',)
    search_fields = ('title', 'body')
    list_filter = ('active', 'category')

@admin.register(Comment)
class Comments(admin.ModelAdmin):
    list_display = ('post', 'name','email', 'comment')


admin.site.register(PostImage)