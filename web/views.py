import logging
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.static import serve

logger = logging.getLogger(__name__)


def serve_media(request, path):
    """Sirve archivos de MEDIA_ROOT (Railway / producción sin nginx dedicado)."""
    media_root = Path(settings.MEDIA_ROOT)
    full_path = media_root / path
    if not full_path.is_file():
        logger.warning("MEDIA 404: path=%r full_path=%r", path, full_path)
    return serve(request, path, document_root=str(settings.MEDIA_ROOT))


def media_debug(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return HttpResponseForbidden("Solo staff")
    media_root = Path(settings.MEDIA_ROOT)
    exists = media_root.is_dir()
    listado = []
    if exists:
        for f in list(media_root.rglob("*"))[:50]:
            if f.is_file():
                listado.append(str(f.relative_to(media_root)))
    body = f"MEDIA_ROOT={media_root}\nexists={exists}\n\n{chr(10).join(listado)}"
    return HttpResponse(body, content_type="text/plain")


class HomeView(TemplateView):
    template_name = "web/home.html"

    def post(self, request, *args, **kwargs):
        nombre = (request.POST.get("nombre") or "").strip()
        apellido = (request.POST.get("apellido") or "").strip()
        email = (request.POST.get("email") or "").strip()
        consulta = (request.POST.get("consulta") or "").strip()
        if not (nombre and apellido and email and consulta):
            messages.error(
                request,
                "Por favor completá todos los campos del formulario.",
            )
        else:
            messages.success(
                request,
                "Gracias por tu mensaje. Te responderemos a la brevedad.",
            )
        return redirect(reverse("web:home") + "#contacto")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["nav_section"] = "inicio"
        return ctx


class EneagramaView(TemplateView):
    template_name = "web/eneagrama.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["nav_section"] = "eneagrama"
        return ctx


class SobreMiView(TemplateView):
    template_name = "web/sobre_mi.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["nav_section"] = "sobre_mi"
        return ctx


class ContactameView(TemplateView):
    template_name = "web/contactame.html"

    def post(self, request, *args, **kwargs):
        nombre = (request.POST.get("nombre") or "").strip()
        apellido = (request.POST.get("apellido") or "").strip()
        email = (request.POST.get("email") or "").strip()
        consulta = (request.POST.get("consulta") or "").strip()
        if not (nombre and apellido and email and consulta):
            messages.error(
                request,
                "Por favor completá todos los campos del formulario.",
            )
        else:
            messages.success(
                request,
                "Gracias por tu mensaje. Te responderemos a la brevedad.",
            )
        return redirect(reverse("web:contactame"))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["nav_section"] = "contactame"
        return ctx
