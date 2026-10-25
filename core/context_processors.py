from django.conf import settings


def site_settings(request):
    return {
        "google_site_verification": settings.GOOGLE_SITE_VERIFICATION,
        "contact_email": settings.CONTACT_EMAIL,
        "adsense_client_id": settings.ADSENSE_CLIENT_ID,
    }
