from django.contrib import admin
from .models import Post, Category
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ['title', 'category', 'created_at']
    summernote_fields = ('content',)
