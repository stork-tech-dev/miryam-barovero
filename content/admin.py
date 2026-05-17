from django.contrib import admin

from .models import NewsItem, Retreat


@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ("title", "published_at", "order", "show_on_home", "is_active")
    list_filter = ("is_active", "show_on_home", "published_at")
    search_fields = ("title", "excerpt", "body")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("order", "-published_at")


@admin.register(Retreat)
class RetreatAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "order", "is_featured", "is_active")
    list_filter = ("is_active", "is_featured")
    search_fields = ("title", "description", "body")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("order", "id")
