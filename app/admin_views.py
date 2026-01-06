from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import datetime, timedelta
import json

from .models import Product, ProductImage, Order, OrderItem, CustomizationDetails, PaymentProof, WebsiteSettings, Banner
from .forms import AdminLoginForm, ProductForm, WebsiteSettingsForm, BannerForm


def is_admin(user):
    return user.is_authenticated and user.is_staff


def admin_login_view(request):
    """Custom admin login"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user and user.is_staff:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid credentials or insufficient permissions.')
    else:
        form = AdminLoginForm()
    
    return render(request, 'admin-portal/login.html', {'form': form})


@user_passes_test(is_admin)
def admin_logout_view(request):
    """Admin logout"""
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('admin_login')


@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard with overview"""
    # Get statistics
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending_payment').count()
    confirmed_orders = Order.objects.filter(status='confirmed').count()
    in_progress_orders = Order.objects.filter(status='in_progress').count()
    completed_orders = Order.objects.filter(status='completed').count()
    
    # Recent orders
    recent_orders = Order.objects.select_related().prefetch_related('items__product').order_by('-created_at')[:5]
    
    # Orders needing attention (pending payment with proof)
    orders_need_attention = Order.objects.filter(
        status='pending_payment',
        payment_proof__isnull=False
    ).count()
    
    # Today's orders
    today = timezone.now().date()
    today_orders = Order.objects.filter(created_at__date=today).count()
    
    context = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'confirmed_orders': confirmed_orders,
        'in_progress_orders': in_progress_orders,
        'completed_orders': completed_orders,
        'recent_orders': recent_orders,
        'orders_need_attention': orders_need_attention,
        'today_orders': today_orders,
    }
    
    return render(request, 'admin-portal/dashboard.html', context)


@user_passes_test(is_admin)
def admin_orders(request):
    """Orders management"""
    status_filter = request.GET.get('status', '')
    search = request.GET.get('search', '')
    
    orders = Order.objects.select_related().prefetch_related('items__product', 'payment_proof')
    
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    if search:
        orders = orders.filter(
            Q(order_id__icontains=search) |
            Q(full_name__icontains=search) |
            Q(mobile_number__icontains=search) |
            Q(email__icontains=search)
        )
    
    orders = orders.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'search': search,
        'status_choices': Order.STATUS_CHOICES,
    }
    
    return render(request, 'admin-portal/orders.html', context)


@user_passes_test(is_admin)
def admin_order_detail(request, order_id):
    """Order detail and management"""
    order = get_object_or_404(Order, order_id=order_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f'Order status updated to {order.get_status_display()}')
            return redirect('admin_order_detail', order_id=order_id)
    
    return render(request, 'admin-portal/order_detail.html', {
        'order': order,
        'status_choices': Order.STATUS_CHOICES,
    })


@user_passes_test(is_admin)
def admin_products(request):
    """Products management"""
    products = Product.objects.prefetch_related('images').order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admin-portal/products.html', {
        'page_obj': page_obj,
    })


@user_passes_test(is_admin)
def admin_product_add(request):
    """Add new product"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            
            # Handle image uploads
            images_data = [
                (form.cleaned_data.get('image_1'), True, 0),  # Primary image
                (form.cleaned_data.get('image_2'), False, 1),
                (form.cleaned_data.get('image_3'), False, 2),
                (form.cleaned_data.get('image_4'), False, 3),
            ]
            
            for image, is_primary, order in images_data:
                if image:
                    ProductImage.objects.create(
                        product=product,
                        image=image,
                        is_primary=is_primary,
                        order=order,
                        alt_text=product.name
                    )
            
            messages.success(request, f'Product "{product.name}" created successfully!')
            return redirect('admin_products')
    else:
        form = ProductForm()
    
    return render(request, 'admin-portal/product_form.html', {
        'form': form,
        'title': 'Add New Product',
    })
#

@user_passes_test(is_admin)
def admin_product_edit(request, product_id):
    """Edit product"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            
            # Handle new image uploads (only if provided)
            images_data = [
                (form.cleaned_data.get('image_1'), True, 0),
                (form.cleaned_data.get('image_2'), False, 1),
                (form.cleaned_data.get('image_3'), False, 2),
                (form.cleaned_data.get('image_4'), False, 3),
            ]
            
            for image, is_primary, order in images_data:
                if image:
                    # Check if image at this order already exists
                    existing_image = product.images.filter(order=order).first()
                    if existing_image:
                        # Update existing image
                        existing_image.image = image
                        existing_image.is_primary = is_primary
                        existing_image.save()
                    else:
                        # Create new image
                        ProductImage.objects.create(
                            product=product,
                            image=image,
                            is_primary=is_primary,
                            order=order,
                            alt_text=product.name
                        )
            
            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('admin_products')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'admin-portal/product_form.html', {
        'form': form,
        'product': product,
        'title': f'Edit {product.name}',
    })


@user_passes_test(is_admin)
def admin_settings(request):
    """Website settings management"""
    settings, created = WebsiteSettings.objects.get_or_create()
    
    if request.method == 'POST':
        form = WebsiteSettingsForm(request.POST, request.FILES, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Website settings updated successfully!')
            return redirect('admin_settings')
    else:
        form = WebsiteSettingsForm(instance=settings)
    
    return render(request, 'admin-portal/settings.html', {
        'form': form,
    })


@user_passes_test(is_admin)
def test_telegram_notification(request):
    """Send a test Telegram notification"""
    try:
        settings = WebsiteSettings.objects.get()
    except WebsiteSettings.DoesNotExist:
        messages.error(request, '❌ Website settings not found.')
        return redirect('admin_settings')
    
    # Check if notifications are enabled
    if not settings.enable_telegram_notifications:
        messages.warning(request, '⚠️ Telegram notifications are disabled. Please enable them in settings.')
        return redirect('admin_settings')
    
    if not settings.telegram_bot_token or not settings.telegram_chat_id:
        messages.error(request, '❌ Please configure Bot Token and Chat ID in settings first.')
        return redirect('admin_settings')
    
    # Send test message
    try:
        from .utils import send_telegram_notification
        from datetime import datetime
        
        test_message = f"""
🧪 <b>Test Notification</b>

✅ Your Telegram bot is working perfectly!

This is a test message sent at:
⏰ {datetime.now().strftime('%d %b %Y, %I:%M %p IST')}

You will receive order notifications like this when customers place orders.

<i>— Sent from Admin Panel</i>
"""
        
        success = send_telegram_notification(test_message, settings)
        
        if success:
            messages.success(request, '✅ Test notification sent successfully! Check your Telegram.')
        else:
            messages.error(request, '❌ Failed to send notification. Check your Bot Token and Chat ID.')
            
    except Exception as e:
        messages.error(request, f'❌ Error: {str(e)}')
    
    return redirect('admin_settings')


@user_passes_test(is_admin)
def admin_banners(request):
    """Banner management"""
    banners = Banner.objects.order_by('order', '-created_at')
    
    return render(request, 'admin-portal/banners.html', {
        'banners': banners,
    })


@user_passes_test(is_admin)
def admin_banner_add(request):
    """Add new banner"""
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            banner = form.save()
            messages.success(request, f'Banner "{banner.title}" created successfully!')
            return redirect('admin_banners')
    else:
        form = BannerForm()
    
    return render(request, 'admin-portal/banner_form.html', {
        'form': form,
        'title': 'Add New Banner',
    })


@user_passes_test(is_admin)
def admin_banner_edit(request, banner_id):
    """Edit banner"""
    banner = get_object_or_404(Banner, id=banner_id)
    
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES, instance=banner)
        if form.is_valid():
            form.save()
            messages.success(request, f'Banner "{banner.title}" updated successfully!')
            return redirect('admin_banners')
    else:
        form = BannerForm(instance=banner)
    
    return render(request, 'admin-portal/banner_form.html', {
        'form': form,
        'banner': banner,
        'title': f'Edit {banner.title}',
    })


@user_passes_test(is_admin)
def admin_banner_delete(request, banner_id):
    """Delete banner"""
    banner = get_object_or_404(Banner, id=banner_id)
    
    if request.method == 'POST':
        banner_title = banner.title
        banner.delete()
        messages.success(request, f'Banner "{banner_title}" deleted successfully!')
        return redirect('admin_banners')
    
    return render(request, 'admin-portal/banner_confirm_delete.html', {
        'banner': banner,
    })


@user_passes_test(is_admin)
def admin_update_order_status(request):
    """AJAX endpoint to update order status"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_id = data.get('order_id')
            new_status = data.get('status')
            
            order = get_object_or_404(Order, order_id=order_id)
            
            if new_status in dict(Order.STATUS_CHOICES):
                order.status = new_status
                order.save()
                
                return JsonResponse({
                    'success': True,
                    'message': f'Order status updated to {order.get_status_display()}',
                    'status_display': order.get_status_display()
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid status'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@user_passes_test(is_admin)
def admin_analytics(request):
    """Simple analytics dashboard"""
    # Order statistics by status
    status_stats = {}
    for status, display in Order.STATUS_CHOICES:
        status_stats[display] = Order.objects.filter(status=status).count()
    
    # Orders by date (last 7 days)
    date_stats = []
    for i in range(7):
        date = timezone.now().date() - timedelta(days=i)
        count = Order.objects.filter(created_at__date=date).count()
        date_stats.append({
            'date': date.strftime('%m/%d'),
            'count': count
        })
    date_stats.reverse()
    
    # Top products
    top_products = OrderItem.objects.values('product__name').annotate(
        total_quantity=Count('quantity')
    ).order_by('-total_quantity')[:5]
    
    context = {
        'status_stats': status_stats,
        'date_stats': date_stats,
        'top_products': top_products,
    }
    
    return render(request, 'admin-portal/analytics.html', context)