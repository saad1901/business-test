from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.http import require_GET
from django.conf import settings as django_settings
from .models import WebsiteSettings
from .utils import generate_qr_image_bytes


@require_GET
def upi_qr(request):
    """Generate and return a QR PNG for the current UPI ID in WebsiteSettings.
    Priority: if WebsiteSettings.upi_id is set, generate QR for it dynamically.
    If not set, but a payment_qr_code exists, stream that file. Otherwise 404.
    
    Query parameters:
    - amount: Optional amount to include in UPI URI (for single product price)
    """
    try:
        ws = WebsiteSettings.objects.get()
    except WebsiteSettings.DoesNotExist:
        return HttpResponseNotFound('No website settings')

    if ws.upi_id:
        try:
            # Get amount from query parameter (for single product price)
            amount = request.GET.get('amount', '')
            
            # Generate a UPI payment URI for better compatibility
            upi_uri = f"upi://pay?pa={ws.upi_id}&pn={ws.site_name or ''}&tn=Payment"
            
            # Add amount if provided (single product price)
            if amount:
                try:
                    # Validate amount is a number
                    float(amount)
                    upi_uri += f"&am={amount}"
                except ValueError:
                    pass  # Skip invalid amount
            
            qr_file = generate_qr_image_bytes(upi_uri)
            return HttpResponse(qr_file.read(), content_type='image/png')
        except Exception as e:
            return HttpResponseNotFound(f'QR generation error: {e}')

    if ws.payment_qr_code:
        # stream the stored file
        with ws.payment_qr_code.open('rb') as f:
            return HttpResponse(f.read(), content_type='image/png')

    return HttpResponseNotFound('No UPI ID or QR code configured')
