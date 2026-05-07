from django.contrib import admin
from django.urls import include, path

from web.views import media_debug, serve_media

admin.site.site_header = "Miryam Barovero — administración"
admin.site.site_title = "Miryam"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("media-debug/", media_debug),
    path("media/<path:path>", serve_media),
    path("", include("web.urls")),
]
