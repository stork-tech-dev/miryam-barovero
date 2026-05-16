import logging

from django.conf import settings
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)


def send_contact_email(*, nombre: str, apellido: str, email: str, consulta: str) -> None:
    subject = f"Consulta web — {nombre} {apellido}"
    body = (
        f"Nueva consulta desde el sitio web de Miryam Barovero.\n\n"
        f"Nombre: {nombre} {apellido}\n"
        f"Email: {email}\n\n"
        f"Consulta:\n{consulta}\n"
    )
    message = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.CONTACT_FORM_RECIPIENT_EMAIL],
        reply_to=[email],
    )
    message.send(fail_silently=False)


def handle_contact_post(request, *, redirect_url: str) -> str:
    """Valida el POST del formulario, envía el mail y devuelve la URL de redirección."""
    nombre = (request.POST.get("nombre") or "").strip()
    apellido = (request.POST.get("apellido") or "").strip()
    email = (request.POST.get("email") or "").strip()
    consulta = (request.POST.get("consulta") or "").strip()

    if not (nombre and apellido and email and consulta):
        from django.contrib import messages

        messages.error(
            request,
            "Por favor completá todos los campos del formulario.",
        )
        return redirect_url

    try:
        send_contact_email(
            nombre=nombre,
            apellido=apellido,
            email=email,
            consulta=consulta,
        )
    except Exception:
        logger.exception("Error al enviar formulario de contacto")
        from django.contrib import messages

        messages.error(
            request,
            "No pudimos enviar tu mensaje. Intentá de nuevo más tarde o escribinos por WhatsApp.",
        )
        return redirect_url

    from django.contrib import messages

    messages.success(
        request,
        "Recibimos tu consulta correctamente. Te responderemos a la brevedad.",
    )
    return redirect_url
