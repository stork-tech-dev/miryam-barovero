from django.contrib import admin

from .models import NewsItem


@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ("title", "published_at", "order", "show_on_home", "is_active")
    list_filter = ("is_active", "show_on_home", "published_at")
    search_fields = ("title", "excerpt", "body")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("order", "-published_at")
