from django.contrib import messages
from django.db.utils import DatabaseError
from django.http import Http404
from django.urls import reverse
from django.views.generic import TemplateView

from content.models import Retreat
from web.forms import RetreatForm
from web.news_views import AdminCreateView, AdminDeleteView, AdminListView, AdminUpdateView


def get_proximos_retiros(max_items=3):
    """Retiros activos para la grilla (hasta 3; huecos vacíos al final)."""
    try:
        retreats = list(
            Retreat.objects.filter(is_active=True).order_by("order", "id")[:max_items]
        )
    except DatabaseError:
        retreats = []

    if not retreats:
        return [None, None, None]

    featured = next((r for r in retreats if r.is_featured), None)
    if featured and featured in retreats:
        others = [r for r in retreats if r.pk != featured.pk]
        ordered = []
        if len(others) > 0:
            ordered.append(others[0])
        ordered.append(featured)
        if len(others) > 1:
            ordered.append(others[1])
        for r in retreats:
            if r not in ordered:
                ordered.append(r)
        retreats = ordered[:max_items]

    while len(retreats) < max_items:
        retreats.append(None)
    return retreats[:max_items]


class RetreatDetailView(TemplateView):
    template_name = "web/retreat_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        retreat = Retreat.objects.filter(slug=slug, is_active=True).first()
        if not retreat:
            raise Http404("Retiro no encontrado.")
        context["nav_section"] = "retiros"
        context["retreat"] = retreat
        return context


class RetreatAdminListView(AdminListView):
    model = Retreat
    section_title = "Retiros"
    section_description = (
        "Gestioná las tarjetas de Próximos retiros (hasta 3 en la página) y su detalle."
    )
    create_url_name = "web:retreat_admin_create"
    list_url_name = "web:retreat_admin_list"
    empty_message = "No hay retiros cargados todavía."

    def get_item_cards(self):
        cards = []
        for item in self.get_queryset():
            cards.append(
                {
                    "id": item.pk,
                    "title": str(item),
                    "order": item.order,
                    "is_active": item.is_active,
                    "edit_url": reverse("web:retreat_admin_update", args=[item.pk]),
                    "delete_url": reverse("web:retreat_admin_delete", args=[item.pk]),
                    "meta": [
                        f"URL: /retiros/{item.slug}/",
                        "Destacado (centro)" if item.is_featured else "Tarjeta normal",
                        item.signup_url or "Inscripción → Contactame",
                    ],
                    "image_url": item.image.url if item.image else None,
                }
            )
        return cards

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_section"] = "admin"
        return context


class RetreatAdminCreateView(AdminCreateView):
    model = Retreat
    form_class = RetreatForm
    section_title = "Crear retiro"
    section_description = "Completá la información del retiro."
    create_url_name = "web:retreat_admin_create"
    list_url_name = "web:retreat_admin_list"
    success_message = "Retiro creado correctamente."

    def get_success_url(self):
        return reverse("web:retreat_admin_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_section"] = "admin"
        return context


class RetreatAdminUpdateView(AdminUpdateView):
    model = Retreat
    form_class = RetreatForm
    section_title = "Editar retiro"
    section_description = "Actualizá la información del retiro."
    create_url_name = "web:retreat_admin_create"
    list_url_name = "web:retreat_admin_list"
    success_message = "Retiro actualizado correctamente."

    def get_success_url(self):
        return reverse("web:retreat_admin_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_section"] = "admin"
        return context


class RetreatAdminDeleteView(AdminDeleteView):
    model = Retreat
    section_title = "Eliminar retiro"
    section_description = "Esta acción no se puede deshacer."
    create_url_name = "web:retreat_admin_create"
    list_url_name = "web:retreat_admin_list"
    success_message = "Retiro eliminado correctamente."

    def get_success_url(self):
        return reverse("web:retreat_admin_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_section"] = "admin"
        return context
