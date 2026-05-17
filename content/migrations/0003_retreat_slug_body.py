from django.db import migrations, models
from django.utils.text import slugify


def fill_retreat_slugs(apps, schema_editor):
    Retreat = apps.get_model("content", "Retreat")
    used = set()
    for retreat in Retreat.objects.all():
        base = slugify(retreat.title) or f"retiro-{retreat.pk}"
        slug = base
        n = 1
        while slug in used:
            slug = f"{base}-{n}"
            n += 1
        retreat.slug = slug
        used.add(slug)
        retreat.save(update_fields=["slug"])


def apply_retreat_slug_body(apps, schema_editor):
    """Idempotente: seguro si un deploy anterior falló a medias."""
    connection = schema_editor.connection
    vendor = connection.vendor

    with connection.cursor() as cursor:
        if vendor == "postgresql":
            cursor.execute(
                "ALTER TABLE content_retreat "
                "ADD COLUMN IF NOT EXISTS body text NOT NULL DEFAULT ''"
            )
            cursor.execute(
                "ALTER TABLE content_retreat "
                "ADD COLUMN IF NOT EXISTS slug varchar(255)"
            )
            cursor.execute("DROP INDEX IF EXISTS content_retreat_slug_e91d12a6_like")
            cursor.execute("DROP INDEX IF EXISTS content_retreat_slug_key")
            cursor.execute("DROP INDEX IF EXISTS content_retreat_slug_uniq")
        elif vendor == "sqlite":
            cursor.execute("PRAGMA table_info(content_retreat)")
            existing = {row[1] for row in cursor.fetchall()}
            if "body" not in existing:
                cursor.execute(
                    "ALTER TABLE content_retreat "
                    "ADD COLUMN body text NOT NULL DEFAULT ''"
                )
            if "slug" not in existing:
                cursor.execute(
                    "ALTER TABLE content_retreat ADD COLUMN slug varchar(255)"
                )

    fill_retreat_slugs(apps, schema_editor)

    with connection.cursor() as cursor:
        if vendor == "postgresql":
            cursor.execute(
                "ALTER TABLE content_retreat ALTER COLUMN slug SET NOT NULL"
            )
            cursor.execute(
                "CREATE UNIQUE INDEX IF NOT EXISTS content_retreat_slug_uniq "
                "ON content_retreat (slug)"
            )
        elif vendor == "sqlite":
            cursor.execute(
                "CREATE UNIQUE INDEX IF NOT EXISTS content_retreat_slug_uniq "
                "ON content_retreat (slug)"
            )


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0002_retreat"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(
                    apply_retreat_slug_body,
                    migrations.RunPython.noop,
                ),
            ],
            state_operations=[
                migrations.AddField(
                    model_name="retreat",
                    name="body",
                    field=models.TextField(blank=True, verbose_name="Contenido completo"),
                ),
                migrations.AddField(
                    model_name="retreat",
                    name="slug",
                    field=models.SlugField(
                        blank=True,
                        max_length=255,
                        unique=True,
                        verbose_name="Slug",
                    ),
                ),
                migrations.AlterField(
                    model_name="retreat",
                    name="description",
                    field=models.TextField(
                        blank=True,
                        help_text="Texto breve que se ve al pasar el mouse sobre la tarjeta.",
                        verbose_name="Resumen en tarjeta",
                    ),
                ),
                migrations.AlterField(
                    model_name="retreat",
                    name="is_featured",
                    field=models.BooleanField(
                        default=False,
                        help_text="Opcional: prioriza este retiro en la columna del medio.",
                        verbose_name="Destacar en el centro",
                    ),
                ),
            ],
        ),
    ]
