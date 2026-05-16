from django.conf import settings


def site_links(request):
    return {
        "url_facebook": settings.SOCIAL_FACEBOOK_URL,
        "url_instagram": settings.SOCIAL_INSTAGRAM_URL,
        "url_whatsapp": settings.SOCIAL_WHATSAPP_URL,
        "url_blog": settings.SOCIAL_BLOG_URL,
    }


def emailjs(request):
    return {
        "emailjs_service_id": settings.EMAILJS_SERVICE_ID,
        "emailjs_template_id": settings.EMAILJS_TEMPLATE_ID,
        "emailjs_public_key": settings.EMAILJS_PUBLIC_KEY,
        "contact_recipient_email": settings.CONTACT_FORM_RECIPIENT_EMAIL,
    }
