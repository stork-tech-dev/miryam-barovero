import logging
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import TemplateView
from django.views.static import serve

from web.enneagram_test import (
    ENNEATYPE_BY_LETTER,
    QUESTIONS,
    VALID_CHOICES,
    calculate_result,
    get_enneagram_emailjs_params,
)

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


class EnneagramTestView(TemplateView):
    template_name = "web/eneagrama_test.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["nav_section"] = "eneagrama"
        ctx["questions"] = QUESTIONS
        ctx["enneatype_by_letter"] = ENNEATYPE_BY_LETTER
        ctx.setdefault("show_result", False)
        return ctx

    def post(self, request, *args, **kwargs):
        nombre = (request.POST.get("nombre") or "").strip()
        email = (request.POST.get("email") or "").strip()
        answers = {}
        valid = True

        for question in QUESTIONS:
            letter = (request.POST.get(question["id"]) or "").strip().upper()
            if letter not in VALID_CHOICES:
                valid = False
                break
            answers[question["id"]] = letter

        if not valid:
            messages.error(
                request,
                "Respondé las cuatro preguntas eligiendo una opción en cada grupo.",
            )
            return self.render_to_response(self.get_context_data())

        result = calculate_result(answers)

        ctx = self.get_context_data()
        ctx["show_result"] = True
        ctx["result"] = result
        ctx["answers"] = answers
        ctx["nombre"] = nombre
        ctx["email"] = email
        ctx["emailjs_payload"] = get_enneagram_emailjs_params(
            nombre=nombre,
            email=email,
            answers=answers,
            result=result,
            to_email=settings.CONTACT_FORM_RECIPIENT_EMAIL,
        )
        return self.render_to_response(ctx)


class RetirosView(TemplateView):
    template_name = "web/retiros.html"

    def get_context_data(self, **kwargs):
        from web.retreat_views import get_proximos_retiros

        ctx = super().get_context_data(**kwargs)
        ctx["nav_section"] = "retiros"
        ctx["proximos_retiros"] = get_proximos_retiros()
        return ctx


class SobreMiView(TemplateView):
    template_name = "web/sobre_mi.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["nav_section"] = "sobre_mi"
        return ctx


class ContactameView(TemplateView):
    template_name = "web/contactame.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["nav_section"] = "contactame"
        consulta = (self.request.GET.get("consulta") or "").strip()
        inscripcion = (self.request.GET.get("inscripcion") or "").strip()
        if consulta:
            ctx["contact_prefill_consulta"] = consulta
        elif inscripcion:
            ctx["contact_prefill_consulta"] = (
                f"Hola, me gustaría inscribirme al retiro «{inscripcion}».\n\n"
                "Quedo a la espera de más información. ¡Gracias!"
            )
        return ctx
