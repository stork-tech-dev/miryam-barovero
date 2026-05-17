from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.utils import DatabaseError
from django.http import Http404
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, TemplateView, UpdateView
from django.views.generic.list import ListView

from content.defaults import DEFAULT_NEWS
from content.models import NewsItem
from web.forms import NewsItemForm


def _normalize_news(item):
    if isinstance(item, dict):
        normalized = item.copy()
        normalized["image_is_media"] = False
        return normalized
    return {
        "title": item.title,
        "slug": item.slug,
        "date": item.published_at,
        "excerpt": item.excerpt,
        "body": item.body,
        "image_url": item.image.url if item.image else None,
        "background_style": None,
        "show_on_home": item.show_on_home,
        "image_is_media": bool(item.image),
    }


def get_news():
    try:
        queryset = NewsItem.objects.filter(is_active=True).order_by("order", "-published_at")
        if queryset.exists():
            return [_normalize_news(item) for item in queryset]
    except DatabaseError:
        pass
    return [_normalize_news(item) for item in DEFAULT_NEWS]


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_staff or user.is_superuser


class PanelBaseMixin(StaffRequiredMixin):
    section_title = ""
    section_description = ""
    create_url_name = ""
    list_url_name = ""
    panel_url_name = "web:panel"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "section_title": self.section_title,
                "section_description": self.section_description,
                "panel_url": reverse(self.panel_url_name),
                "create_url": reverse(self.create_url_name) if self.create_url_name else None,
                "list_url": reverse(self.list_url_name) if self.list_url_name else None,
                "model_name": getattr(
                    getattr(self, "model", None), "_meta", None
                ).model_name
                if getattr(self, "model", None)
                else "",
            }
        )
        return context


class AdminListView(PanelBaseMixin, ListView):
    template_name = "web/content_list.html"
    context_object_name = "items"
    empty_message = "No hay elementos cargados todavía."

    def get_item_cards(self):
        cards = []
        for item in self.get_queryset():
            card = {
                "id": item.pk,
                "title": str(item),
                "order": item.order,
                "is_active": item.is_active,
                "edit_url": reverse("web:news_admin_update", args=[item.pk]),
                "delete_url": reverse("web:news_admin_delete", args=[item.pk]),
                "meta": [
                    f"Fecha: {item.published_at:%d/%m/%Y}",
                    "Visible en inicio" if item.show_on_home else "Solo listado",
                    item.slug,
                ],
                "image_url": item.image.url if item.image else None,
            }
            cards.append(card)
        return cards

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item_cards"] = self.get_item_cards()
        context["empty_message"] = self.empty_message
        return context


class AdminCreateView(PanelBaseMixin, CreateView):
    template_name = "web/content_form.html"
    success_message = "Elemento creado correctamente."

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class AdminUpdateView(PanelBaseMixin, UpdateView):
    template_name = "web/content_form.html"
    success_message = "Elemento actualizado correctamente."

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class AdminDeleteView(PanelBaseMixin, DeleteView):
    template_name = "web/content_confirm_delete.html"
    success_message = "Elemento eliminado correctamente."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class PanelView(StaffRequiredMixin, TemplateView):
    template_name = "web/panel.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_section"] = "admin"
        context["admin_links"] = [
            {
                "title": "Novedades",
                "description": (
                    "Crear, editar y ordenar las novedades visibles en inicio y en la página interna."
                ),
                "url": reverse("web:news_admin_list"),
            },
            {
                "title": "Retiros",
                "description": (
                    "Gestionar las tarjetas de Próximos retiros en la página Retiros (hasta 3)."
                ),
                "url": reverse("web:retreat_admin_list"),
            },
        ]
        return context


class NewsAdminListView(AdminListView):
    model = NewsItem
    section_title = "Novedades"
    section_description = "Gestioná el contenido, imagen, orden y visibilidad de las novedades."
    create_url_name = "web:news_admin_create"
    list_url_name = "web:news_admin_list"
    empty_message = "No hay novedades cargadas todavía."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_section"] = "admin"
        return context


class NewsAdminCreateView(AdminCreateView):
    model = NewsItem
    form_class = NewsItemForm
    section_title = "Crear novedad"
    section_description = "Completá la información de la novedad."
    create_url_name = "web:news_admin_create"
    list_url_name = "web:news_admin_list"
    success_message = "Novedad creada correctamente."

    def get_success_url(self):
        return reverse("web:news_admin_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_section"] = "admin"
        return context


class NewsAdminUpdateView(AdminUpdateView):
    model = NewsItem
    form_class = NewsItemForm
    section_title = "Editar novedad"
    section_description = "Actualizá la información de la novedad."
    create_url_name = "web:news_admin_create"
    list_url_name = "web:news_admin_list"
    success_message = "Novedad actualizada correctamente."

    def get_success_url(self):
        return reverse("web:news_admin_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_section"] = "admin"
        return context


class NewsAdminDeleteView(AdminDeleteView):
    model = NewsItem
    section_title = "Eliminar novedad"
    section_description = "Esta acción no se puede deshacer."
    create_url_name = "web:news_admin_create"
    list_url_name = "web:news_admin_list"
    success_message = "Novedad eliminada correctamente."

    def get_success_url(self):
        return reverse("web:news_admin_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_section"] = "admin"
        return context


class NewsListView(TemplateView):
    template_name = "web/news_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_section"] = "novedades"
        context["news_items"] = get_news()
        return context


class NewsDetailView(TemplateView):
    template_name = "web/news_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        news_item = NewsItem.objects.filter(slug=slug, is_active=True).first()
        if news_item:
            item = _normalize_news(news_item)
        else:
            item = next((n for n in DEFAULT_NEWS if n.get("slug") == slug), None)
            if item:
                item = item.copy()
                item["image_is_media"] = False
        if not item:
            raise Http404("Novedad no encontrada.")
        context["nav_section"] = "novedades"
        context["item"] = item
        return context
