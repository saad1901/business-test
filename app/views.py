from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.db.models import Q
from decimal import Decimal
import json

from .models import Product, Order, OrderItem, CustomizationDetails, PaymentProof, WebsiteSettings, Banner
from .forms import CustomOrderForm, CustomizationForm, PaymentProofForm, OrderTrackingForm


def home(request):
    """Landing page with featured products and banners"""
    featured_products = Product.objects.filter(is_active=True)[:6]
    banners = Banner.objects.filter(is_active=True, banner_type='hero')[:3]
    
    # Get website settings
    try:
        settings = WebsiteSettings.objects.first()
    except WebsiteSettings.DoesNotExist:
        settings = None
    
    return render(request, 'app/home.html', {
        'featured_products': featured_products,
        'banners': banners,
        'settings': settings
    })


class ProductListView(ListView):
    model = Product
    template_name = 'app/product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        return Product.objects.filter(is_active=True).prefetch_related('images')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'app/product_detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customization_form'] = CustomizationForm()
        return context


def create_order(request, product_id):
    """Handle custom order creation"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    # Get website settings for payment info
    try:
        website_settings = WebsiteSettings.objects.get()
    except WebsiteSettings.DoesNotExist:
        website_settings = None
    
    if request.method == 'POST':
        # Check for duplicate submission (within last 10 seconds)
        last_order_time = request.session.get('last_order_time')
        if last_order_time:
            from datetime import datetime, timedelta
            last_time = datetime.fromisoformat(last_order_time)
            if datetime.now() - last_time < timedelta(seconds=10):
                messages.warning(request, '⚠️ Please wait a moment before placing another order.')
                return redirect('product_detail', pk=product_id)
        
        customization_form = CustomizationForm(request.POST, request.FILES)
        order_form = CustomOrderForm(request.POST)
        payment_form = PaymentProofForm(request.POST, request.FILES)
        
        if customization_form.is_valid() and order_form.is_valid() and payment_form.is_valid():
            try:
                with transaction.atomic():
                    # Create order
                    order = order_form.save(commit=False)
                    if request.user.is_authenticated:
                        order.user = request.user
                    
                    quantity = customization_form.cleaned_data['quantity']
                    unit_price = product.base_price
                    total_price = unit_price * quantity
                    order.total_amount = total_price
                    order.save()
                    
                    # Create order item
                    order_item = OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        unit_price=unit_price,
                        total_price=total_price
                    )
                    
                    # Create customization details
                    customization = customization_form.save(commit=False)
                    customization.order_item = order_item
                    customization.save()
                    
                    # Create payment proof
                    payment_proof = payment_form.save(commit=False)
                    payment_proof.order = order
                    payment_proof.save()
                    
                    # Send Telegram notification
                    try:
                        from .utils import send_telegram_notification_with_buttons
                        notification_sent = send_telegram_notification_with_buttons(order, website_settings)
                        if notification_sent:
                            print(f"✅ Telegram notification sent for order {order.order_id}")
                        else:
                            print(f"⚠️ Telegram notification failed for order {order.order_id}")
                            print(f"   - Notifications enabled: {website_settings.enable_telegram_notifications if website_settings else 'No settings'}")
                            print(f"   - Bot token exists: {bool(website_settings.telegram_bot_token) if website_settings else False}")
                            print(f"   - Chat ID exists: {bool(website_settings.telegram_chat_id) if website_settings else False}")
                    except Exception as e:
                        # Don't break order flow if notification fails
                        print(f"❌ Notification error: {e}")
                        import traceback
                        traceback.print_exc()
                    
                    # Set last order time to prevent duplicates
                    from datetime import datetime
                    request.session['last_order_time'] = datetime.now().isoformat()
                    
                    # Clear pending order session
                    if 'pending_order_id' in request.session:
                        del request.session['pending_order_id']
                    
                    messages.success(request, 'Order placed successfully! We have received your payment proof and will verify it shortly.')
                    return redirect('order_confirmation', order_id=order.order_id)
                    
            except Exception as e:
                messages.error(request, 'Error creating order. Please try again.')
                print(f"Order creation error: {e}")
                import traceback
                traceback.print_exc()
                
    else:
        customization_form = CustomizationForm()
        order_form = CustomOrderForm()
        payment_form = PaymentProofForm()
    
    return render(request, 'app/create_order.html', {
        'product': product,
        'customization_form': customization_form,
        'order_form': order_form,
        'payment_form': payment_form,
        'website_settings': website_settings
    })


def payment_view(request, order_id):
    """Handle payment and proof upload"""
    order = get_object_or_404(Order, order_id=order_id, status='pending_payment')
    
    # Check if user has permission to view this order
    if not (request.session.get('pending_order_id') == str(order_id) or 
            (request.user.is_authenticated and order.user == request.user)):
        messages.error(request, 'You do not have permission to view this order.')
        return redirect('home')
    
    if request.method == 'POST':
        payment_form = PaymentProofForm(request.POST, request.FILES)
        if payment_form.is_valid():
            payment_proof = payment_form.save(commit=False)
            payment_proof.order = order
            payment_proof.save()
            
            # Clear session
            if 'pending_order_id' in request.session:
                del request.session['pending_order_id']
            
            messages.success(request, 'Payment proof uploaded successfully!')
            return redirect('order_confirmation', order_id=order.order_id)
    else:
        payment_form = PaymentProofForm()
    
    # Get UPI details from settings
    try:
        settings = WebsiteSettings.objects.first()
        upi_details = {
            'upi_id': settings.upi_id if settings else 'resinart@paytm',
            'amount': order.total_amount,
            'merchant_name': settings.site_name if settings else 'Custom Resin Art'
        }
    except:
        upi_details = {
            'upi_id': 'resinart@paytm',
            'amount': order.total_amount,
            'merchant_name': 'Custom Resin Art'
        }
    
    return render(request, 'app/payment.html', {
        'order': order,
        'payment_form': payment_form,
        'upi_details': upi_details
    })


def order_confirmation(request, order_id):
    """Order confirmation page"""
    order = get_object_or_404(Order, order_id=order_id)
    
    # Allow access if user has payment proof or is authenticated user
    if not (hasattr(order, 'payment_proof') or 
            (request.user.is_authenticated and order.user == request.user)):
        messages.error(request, 'Order not found.')
        return redirect('home')
    
    return render(request, 'app/order_confirmation.html', {
        'order': order
    })


def track_order(request):
    """Order tracking page"""
    form = OrderTrackingForm()
    orders = []
    
    if request.method == 'POST':
        form = OrderTrackingForm(request.POST)
        if form.is_valid():
            tracking_info = form.cleaned_data['tracking_info'].strip()
            
            # Search by mobile number or email
            orders = Order.objects.filter(
                Q(mobile_number__icontains=tracking_info) | 
                Q(email__iexact=tracking_info)
            ).prefetch_related('items__product', 'items__customization').order_by('-created_at')
            
            if not orders:
                messages.warning(request, 'No orders found with the provided information.')
    
    return render(request, 'app/track_order.html', {
        'form': form,
        'orders': orders
    })


def calculate_price(request):
    """AJAX endpoint for price calculation"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = int(data.get('quantity', 1))
            
            product = get_object_or_404(Product, id=product_id)
            total_price = product.base_price * quantity
            
            return JsonResponse({
                'success': True,
                'unit_price': float(product.base_price),
                'total_price': float(total_price),
                'formatted_total': f"₹{total_price:,.2f}"
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})