from django.db import models
from django.utils.text import slugify


class OrderedActiveModel(models.Model):
    order = models.PositiveIntegerField("Orden", default=0)
    is_active = models.BooleanField("Activo", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("order", "id")


class NewsItem(OrderedActiveModel):
    """Novedades / blog — gestión desde el admin de Django."""

    title = models.CharField("Título", max_length=255)
    slug = models.SlugField("Slug", max_length=255, unique=True, blank=True)
    image = models.ImageField("Imagen", upload_to="news/", blank=True, null=True)
    excerpt = models.TextField("Resumen")
    body = models.TextField("Contenido", blank=True)
    published_at = models.DateField("Fecha")
    show_on_home = models.BooleanField("Mostrar en inicio", default=True)

    class Meta(OrderedActiveModel.Meta):
        verbose_name = "Novedad"
        verbose_name_plural = "Novedades"
        ordering = ("order", "-published_at", "id")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
