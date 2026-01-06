from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Product, ProductImage, Order, OrderItem, CustomizationDetails, PaymentProof, WebsiteSettings, Banner


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Preview"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'base_price', 'customization_type', 'is_active', 'created_at']
    list_filter = ['customization_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    inlines = [ProductImageInline]
    list_editable = ['is_active']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'unit_price', 'total_price', 'customization_preview']
    
    def customization_preview(self, obj):
        if hasattr(obj, 'customization'):
            custom = obj.customization
            html = []
            if custom.custom_text:
                html.append(f'<strong>Text:</strong> "{custom.custom_text}"')
            if custom.custom_image:
                html.append(f'<strong>Image:</strong> <img src="{custom.image.url}" style="max-height: 30px; max-width: 30px;" />')
            if custom.notes:
                html.append(f'<strong>Notes:</strong> {custom.notes}')
            return format_html('<br>'.join(html)) if html else 'No customization'
        return 'No customization'
    customization_preview.short_description = "Customization"


class PaymentProofInline(admin.TabularInline):
    model = PaymentProof
    extra = 0
    readonly_fields = ['screenshot_preview', 'uploaded_at']
    
    def screenshot_preview(self, obj):
        if obj.screenshot:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="max-height: 100px; max-width: 100px;" /></a>',
                obj.screenshot.url, obj.screenshot.url
            )
        return "No screenshot"
    screenshot_preview.short_description = "Payment Screenshot"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id_short', 'full_name', 'mobile_number', 'status', 'total_amount', 'created_at', 'payment_status']
    list_filter = ['status', 'created_at']
    search_fields = ['order_id', 'full_name', 'mobile_number', 'email']
    readonly_fields = ['order_id', 'created_at', 'updated_at', 'order_summary']
    inlines = [OrderItemInline, PaymentProofInline]
    list_editable = ['status']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_id', 'status', 'total_amount', 'created_at', 'updated_at')
        }),
        ('Customer Details', {
            'fields': ('full_name', 'mobile_number', 'email', 'delivery_address')
        }),
        ('Order Summary', {
            'fields': ('order_summary',),
            'classes': ('collapse',)
        })
    )
    
    def order_id_short(self, obj):
        return str(obj.order_id)[:8] + '...'
    order_id_short.short_description = 'Order ID'
    
    def status_badge(self, obj):
        colors = {
            'pending_payment': '#ffc107',
            'confirmed': '#17a2b8',
            'in_progress': '#007bff',
            'completed': '#28a745',
            'cancelled': '#dc3545'
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def payment_status(self, obj):
        if hasattr(obj, 'payment_proof'):
            return format_html('<span style="color: green;">✓ Proof Uploaded</span>')
        return format_html('<span style="color: red;">✗ No Proof</span>')
    payment_status.short_description = 'Payment'
    
    def order_summary(self, obj):
        items_html = []
        for item in obj.items.all():
            items_html.append(f"• {item.product.name} x {item.quantity} = ₹{item.total_price}")
        return format_html('<br>'.join(items_html))
    order_summary.short_description = 'Items'
    
    # Mobile-friendly admin
    class Media:
        css = {
            'all': ('admin/css/mobile-admin.css',)
        }


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'unit_price', 'total_price']
    list_filter = ['product', 'order__status']
    readonly_fields = ['total_price']


@admin.register(CustomizationDetails)
class CustomizationDetailsAdmin(admin.ModelAdmin):
    list_display = ['order_item', 'custom_text', 'has_image', 'notes_preview']
    search_fields = ['custom_text', 'notes']
    readonly_fields = ['image_preview']
    
    def has_image(self, obj):
        return bool(obj.custom_image)
    has_image.boolean = True
    has_image.short_description = 'Has Image'
    
    def notes_preview(self, obj):
        return obj.notes[:50] + '...' if len(obj.notes) > 50 else obj.notes
    notes_preview.short_description = 'Notes'
    
    def image_preview(self, obj):
        if obj.custom_image:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 200px;" />', obj.custom_image.url)
        return "No image uploaded"
    image_preview.short_description = "Customer Image"


@admin.register(PaymentProof)
class PaymentProofAdmin(admin.ModelAdmin):
    list_display = ['order', 'upi_transaction_id', 'uploaded_at', 'screenshot_preview']
    list_filter = ['uploaded_at']
    readonly_fields = ['uploaded_at', 'large_screenshot_preview']
    
    def screenshot_preview(self, obj):
        if obj.screenshot:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.screenshot.url)
        return "No screenshot"
    screenshot_preview.short_description = "Preview"
    
    def large_screenshot_preview(self, obj):
        if obj.screenshot:
            return format_html('<img src="{}" style="max-height: 400px; max-width: 400px;" />', obj.screenshot.url)
        return "No screenshot uploaded"
    large_screenshot_preview.short_description = "Payment Screenshot"


@admin.register(WebsiteSettings)
class WebsiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'tagline', 'address')
        }),
        ('Contact Details', {
            'fields': ('contact_phone', 'contact_email', 'whatsapp_number', 'upi_id')
        }),
        ('Social Media', {
            'fields': ('instagram_url', 'facebook_url'),
            'classes': ('collapse',)
        }),
        ('Business Settings', {
            'fields': ('processing_time_days', 'delivery_time_days')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ['created_at', 'updated_at']
    
    def has_add_permission(self, request):
        # Only allow one settings instance
        return not WebsiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'banner_type', 'is_active', 'order', 'image_preview', 'created_at']
    list_filter = ['banner_type', 'is_active', 'created_at']
    list_editable = ['is_active', 'order']
    search_fields = ['title', 'subtitle']
    
    fieldsets = (
        ('Banner Content', {
            'fields': ('title', 'subtitle', 'banner_type', 'image')
        }),
        ('Link Settings', {
            'fields': ('link_url', 'link_text'),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order')
        })
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Preview"


# Customize admin site
admin.site.site_header = "Leena's Craft Admin"
admin.site.site_title = "Leena's Craft"
admin.site.index_title = "Business Management"
