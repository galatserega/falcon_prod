from django.contrib import admin
from .models import News, Comment
from django.utils.html import format_html
# Register your models here.

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'formatted_content')
    prepopulated_fields = {'slug': ('title',)}

    def formatted_content(self, obj):
        return format_html(obj.content)
    formatted_content.short_description = 'Content'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('news', 'user', 'created_at')
