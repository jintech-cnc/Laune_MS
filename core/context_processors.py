from .models import ServiceDomain


def site_context(request):
    return {
        'nav_services': ServiceDomain.objects.filter(is_active=True)[:8],
        'site_name': 'La Une Multiservice',
        'site_tagline': "L'excellence à votre service",
        'site_phone': '+243 970 202 552',
        'site_email': 'contact@launemultiservice.com',
        'site_address': 'Kolwezi, RDC',
    }
