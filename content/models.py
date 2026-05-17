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


class Retreat(OrderedActiveModel):
    """Próximos retiros — tarjetas en la página Retiros y detalle propio."""

    title = models.CharField("Título", max_length=255)
    slug = models.SlugField("Slug", max_length=255, unique=True, blank=True)
    description = models.TextField(
        "Resumen en tarjeta",
        blank=True,
        help_text="Texto breve que se ve al pasar el mouse sobre la tarjeta.",
    )
    body = models.TextField(
        "Contenido completo",
        blank=True,
        help_text="Texto de la página de detalle del retiro.",
    )
    image = models.ImageField("Imagen de fondo", upload_to="retreats/", blank=True, null=True)
    signup_url = models.URLField(
        "Enlace de inscripción",
        blank=True,
        help_text="Opcional. Si está vacío, el botón lleva a Contactame.",
    )
    is_featured = models.BooleanField(
        "Destacar en el centro",
        default=False,
        help_text="Opcional: prioriza este retiro en la columna del medio.",
    )

    class Meta(OrderedActiveModel.Meta):
        verbose_name = "Retiro"
        verbose_name_plural = "Retiros"
        ordering = ("order", "id")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_inscripcion_contact_url(self):
        from urllib.parse import urlencode

        from django.urls import reverse

        if self.signup_url:
            return self.signup_url
        mensaje = (
            f"Hola, me gustaría inscribirme al retiro «{self.title}».\n\n"
            "Quedo a la espera de más información. ¡Gracias!"
        )
        params = urlencode({"inscripcion": self.title, "consulta": mensaje})
        return f"{reverse('web:contactame')}?{params}"
