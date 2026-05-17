from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Retreat",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("order", models.PositiveIntegerField(default=0, verbose_name="Orden")),
                ("is_active", models.BooleanField(default=True, verbose_name="Activo")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=255, verbose_name="Título")),
                ("description", models.TextField(blank=True, verbose_name="Descripción")),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="retreats/",
                        verbose_name="Imagen de fondo",
                    ),
                ),
                (
                    "signup_url",
                    models.URLField(
                        blank=True,
                        help_text="Opcional. Si está vacío, el botón lleva a Contactame.",
                        verbose_name="Enlace de inscripción",
                    ),
                ),
                (
                    "is_featured",
                    models.BooleanField(
                        default=False,
                        help_text="Muestra título, descripción y botón Inscribirme sobre la imagen.",
                        verbose_name="Tarjeta destacada (centro)",
                    ),
                ),
            ],
            options={
                "verbose_name": "Retiro",
                "verbose_name_plural": "Retiros",
                "ordering": ("order", "id"),
            },
        ),
    ]
