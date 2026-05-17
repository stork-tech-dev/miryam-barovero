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


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0002_retreat"),
    ]

    operations = [
        migrations.AddField(
            model_name="retreat",
            name="body",
            field=models.TextField(blank=True, verbose_name="Contenido completo"),
        ),
        migrations.AddField(
            model_name="retreat",
            name="slug",
            field=models.SlugField(blank=True, max_length=255, null=True, verbose_name="Slug"),
        ),
        migrations.RunPython(fill_retreat_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="retreat",
            name="slug",
            field=models.SlugField(blank=True, max_length=255, unique=True, verbose_name="Slug"),
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
    ]
