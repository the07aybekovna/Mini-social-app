from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['caption', 'author', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['caption', 'author__username']
    readonly_fields = ['created_at', 'updated_at']
