from django.contrib import admin
from .models import Post, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'approved']
    list_filter = ['approved', 'created_at']
    search_fields = ['title', 'content']
    actions = ['approve_posts']

    def approve_posts(self, request, queryset):
        queryset.update(approved=True)
    approve_posts.short_description = 'Approve selected posts'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
