from io import BytesIO
from datetime import datetime
from django.core.files.base import ContentFile


def generate_qr_image_bytes(data):
    """Generate PNG bytes for a QR code of the given data.
    Uses the `qrcode` library; caller should handle ImportError if it's not installed.
    Returns a tuple (ContentFile, filename) suitable for saving to an ImageField.
    """
    import qrcode
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    filename = f"upi_qr_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    return ContentFile(buffer.read(), name=filename)


def send_telegram_notification(message, settings=None):
    """
    Send a notification via Telegram Bot.
    
    Args:
        message: The message text to send
        settings: WebsiteSettings instance (optional, will fetch if not provided)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        import requests
    except ImportError:
        print("❌ requests library not installed. Run: pip install requests")
        return False
    
    if settings is None:
        from .models import WebsiteSettings
        try:
            settings = WebsiteSettings.objects.get()
        except WebsiteSettings.DoesNotExist:
            print("❌ WebsiteSettings not found")
            return False
    
    # Check if Telegram notifications are enabled
    if not settings.enable_telegram_notifications:
        print("⚠️ Telegram notifications are disabled in settings")
        return False
    
    if not settings.telegram_bot_token:
        print("❌ Telegram Bot Token is not configured")
        return False
        
    if not settings.telegram_chat_id:
        print("❌ Telegram Chat ID is not configured")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
        data = {
            'chat_id': settings.telegram_chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        print(f"📤 Sending Telegram notification to chat {settings.telegram_chat_id}...")
        response = requests.post(url, data=data, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ Telegram notification sent successfully!")
            return True
        else:
            print(f"❌ Telegram API error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error sending Telegram notification: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error sending Telegram notification: {e}")
        import traceback
        traceback.print_exc()
        return False


def format_order_notification(order):
    """
    Format an order into a Telegram notification message.
    
    Args:
        order: Order instance
    
    Returns:
        str: Formatted message
    """
    items_text = ""
    for item in order.items.all():
        # Basic item info
        items_text += f"\n\n📦 <b>{item.product.name}</b>"
        items_text += f"\n   💰 ₹{item.unit_price} × {item.quantity} = ₹{item.total_price}"
        items_text += f"\n   🎨 Type: {item.product.get_customization_type_display()}"
        
        # Customization details if exists
        if hasattr(item, 'customization') and item.customization:
            custom = item.customization
            items_text += f"\n   <b>✨ Customization:</b>"
            
            # Custom text
            if custom.custom_text:
                items_text += f"\n      📝 Text: <i>\"{custom.custom_text}\"</i>"
            
            # Custom image
            if custom.custom_image:
                items_text += f"\n      🖼️ Image: Uploaded (check admin portal)"
            
            # Special notes
            if custom.notes:
                items_text += f"\n      📌 Notes: <i>{custom.notes}</i>"
    
    # Get payment proof URL if exists
    payment_proof_text = ""
    if hasattr(order, 'payment_proof') and order.payment_proof.screenshot:
        try:
            # Get the website URL from settings
            from .models import WebsiteSettings
            try:
                ws = WebsiteSettings.objects.get()
                domain = ws.website_url.rstrip('/')
            except:
                domain = "http://localhost:8000"  # Fallback
            
            screenshot_url = f"{domain}{order.payment_proof.screenshot.url}"
            payment_proof_text = f'\n\n💳 <a href="{screenshot_url}">View Payment Screenshot</a>'
        except:
            payment_proof_text = "\n\n✅ Payment proof uploaded"
    else:
        payment_proof_text = "\n\n⚠️ Payment proof pending"
    
    message = f"""
🔔 <b>New Order Received!</b>

📦 <b>Order ID:</b> <code>{order.order_id}</code>

👤 <b>Customer Details:</b>
   Name: {order.full_name}
   📱 Phone: {order.mobile_number}
   {f'📧 Email: {order.email}' if order.email else ''}

🛍️ <b>Order Items:</b>{items_text}

💰 <b>Total Amount: ₹{order.total_amount}</b>

📍 <b>Delivery Address:</b>
{order.delivery_address}

⏰ <b>Order Time:</b> {order.created_at.astimezone().strftime('%d %b %Y, %I:%M %p IST')}{payment_proof_text}
"""
    return message.strip()


def send_telegram_notification_with_buttons(order, settings=None):
    """
    Send a notification with inline buttons via Telegram Bot.
    
    Args:
        order: Order instance
        settings: WebsiteSettings instance (optional, will fetch if not provided)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        import requests
    except ImportError:
        print("❌ requests library not installed. Run: pip install requests")
        return False
    
    if settings is None:
        from .models import WebsiteSettings
        try:
            settings = WebsiteSettings.objects.get()
        except WebsiteSettings.DoesNotExist:
            print("❌ WebsiteSettings not found")
            return False
    
    # Check if Telegram notifications are enabled
    if not settings.enable_telegram_notifications:
        print("⚠️ Telegram notifications are disabled in settings")
        return False
    
    if not settings.telegram_bot_token:
        print("❌ Telegram Bot Token is not configured")
        return False
        
    if not settings.telegram_chat_id:
        print("❌ Telegram Chat ID is not configured")
        return False
    
    try:
        # Format the message
        message = format_order_notification(order)
        
        # Get website URL from settings
        domain = settings.website_url.rstrip('/') if settings.website_url else "http://localhost:8000"
        
        # Check if domain is localhost (not valid for Telegram buttons)
        is_localhost = 'localhost' in domain or '127.0.0.1' in domain
        
        # Build the admin order detail URL (only if not localhost)
        admin_url = f"{domain}/admin-portal/orders/{order.order_id}/" if not is_localhost else None
        
        # Create buttons
        buttons = []
        
        # First row: WhatsApp
        if order.mobile_number:
            # WhatsApp button
            whatsapp_number = order.mobile_number.replace('+', '').replace(' ', '').replace('-', '')
            # Add country code if not present
            if not whatsapp_number.startswith('91') and len(whatsapp_number) == 10:
                whatsapp_number = '91' + whatsapp_number
            whatsapp_url = f"https://wa.me/{whatsapp_number}"
            buttons.append([{
                "text": "💬 WhatsApp Customer",
                "url": whatsapp_url
            }])
        
        # Second row: View Order Details (only if not localhost)
        if admin_url:
            buttons.append([{
                "text": "🔍 View Order Details",
                "url": admin_url
            }])
        
        # Third row: Payment Screenshot (if exists and not localhost)
        if not is_localhost and hasattr(order, 'payment_proof') and order.payment_proof.screenshot:
            try:
                screenshot_url = f"{domain}{order.payment_proof.screenshot.url}"
                buttons.append([{
                    "text": "💳 View Payment Screenshot",
                    "url": screenshot_url
                }])
            except:
                pass
        
        url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
        data = {
            'chat_id': settings.telegram_chat_id,
            'text': message,
            'parse_mode': 'HTML',
            'reply_markup': {
                'inline_keyboard': buttons
            }
        }
        
        print(f"📤 Sending Telegram notification with buttons to chat {settings.telegram_chat_id}...")
        response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ Telegram notification sent successfully!")
            return True
        else:
            print(f"❌ Telegram API error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error sending Telegram notification: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error sending Telegram notification: {e}")
        import traceback
        traceback.print_exc()
        return False
