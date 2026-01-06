from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
import uuid


class Product(models.Model):
    CUSTOMIZATION_CHOICES = [
        ('text', 'Text Only'),
        ('photo', 'Photo Only'),
        ('both', 'Text and Photo'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    customization_type = models.CharField(max_length=10, choices=CUSTOMIZATION_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.product.name} - Image {self.order}"
    
    class Meta:
        ordering = ['order']


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending_payment', 'Payment Verification Pending'),
        ('confirmed', 'Order Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Customer details
    full_name = models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    delivery_address = models.TextField()
    
    # Order details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_payment')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order {self.order_id} - {self.full_name}"
    
    class Meta:
        ordering = ['-created_at']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class CustomizationDetails(models.Model):
    order_item = models.OneToOneField(OrderItem, on_delete=models.CASCADE, related_name='customization')
    custom_text = models.CharField(max_length=500, blank=True)
    custom_image = models.ImageField(upload_to='customizations/', blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Customization for {self.order_item}"


class PaymentProof(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment_proof')
    screenshot = models.ImageField(upload_to='payment_proofs/')
    upi_transaction_id = models.CharField(max_length=100, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment proof for {self.order.order_id}"


class WebsiteSettings(models.Model):
    site_name = models.CharField(max_length=200, default="Leena's Craft")
    tagline = models.CharField(max_length=500, default='Beautiful Personalized Resin Keychains & Gifts')
    website_url = models.URLField(blank=True, default='http://localhost:8000', help_text='Your website URL (e.g., https://yoursite.com)')
    contact_phone = models.CharField(max_length=15, default='+91 XXXXXXXXXX')
    contact_email = models.EmailField(default='info@customresinart.com')
    upi_id = models.CharField(max_length=100, default='resinart@paytm')
    payment_qr_code = models.ImageField(upload_to='payment/', blank=True, null=True, help_text='QR code image for payment')
    whatsapp_number = models.CharField(max_length=15, default='+91 XXXXXXXXXX')
    address = models.TextField(default='India')
    
    # Social media
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    
    # Notification settings
    telegram_bot_token = models.CharField(max_length=200, blank=True, help_text='Telegram Bot Token for order notifications')
    telegram_chat_id = models.CharField(max_length=100, blank=True, help_text='Your Telegram Chat ID to receive notifications')
    enable_telegram_notifications = models.BooleanField(default=False, help_text='Enable Telegram notifications for new orders')
    
    # Business settings
    processing_time_days = models.PositiveIntegerField(default=5, help_text='Days to process orders')
    delivery_time_days = models.PositiveIntegerField(default=7, help_text='Days for delivery')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Website Settings'
        verbose_name_plural = 'Website Settings'
    
    def __str__(self):
        return f"Website Settings - {self.site_name}"
    
    def save(self, *args, **kwargs):
        # Ensure only one settings instance exists
        if not self.pk and WebsiteSettings.objects.exists():
            raise ValueError('Only one WebsiteSettings instance is allowed')
        super().save(*args, **kwargs)


class Banner(models.Model):
    BANNER_TYPES = [
        ('hero', 'Hero Banner'),
        ('promotion', 'Promotion Banner'),
        ('announcement', 'Announcement Banner'),
    ]
    
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=500, blank=True)
    banner_type = models.CharField(max_length=20, choices=BANNER_TYPES, default='hero')
    image = models.ImageField(upload_to='banners/')
    link_url = models.URLField(blank=True, help_text='Optional link when banner is clicked')
    link_text = models.CharField(max_length=100, blank=True, help_text='Button text for the link')
    
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text='Display order (lower numbers first)')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.get_banner_type_display()} - {self.title}"
