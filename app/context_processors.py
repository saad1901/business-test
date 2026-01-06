from .models import WebsiteSettings


def website_settings(request):
    """Make website settings available in all templates"""
    try:
        settings = WebsiteSettings.objects.first()
    except WebsiteSettings.DoesNotExist:
        settings = None
    
    return {
        'settings': settings
    }