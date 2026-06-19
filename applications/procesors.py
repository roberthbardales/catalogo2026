from django.conf import settings

def whatsapp_number(request):
    return {'whatsapp_number': settings.WHATSAPP_NUMBER}
