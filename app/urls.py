from django.urls import path
from django.contrib.auth import views as auth_views
from . import views, admin_views, views_qr

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    
    # Order flow
    path('order/<int:product_id>/', views.create_order, name='create_order'),
    path('payment/<uuid:order_id>/', views.payment_view, name='payment'),
    path('confirmation/<uuid:order_id>/', views.order_confirmation, name='order_confirmation'),
    
    # Order tracking
    path('track-order/', views.track_order, name='track_order'),
    
    # Custom Admin Portal
    path('admin-portal/', admin_views.admin_login_view, name='admin_login'),
    path('admin-portal/logout/', admin_views.admin_logout_view, name='admin_logout'),
    path('admin-portal/dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin-portal/orders/', admin_views.admin_orders, name='admin_orders'),
    path('admin-portal/orders/<uuid:order_id>/', admin_views.admin_order_detail, name='admin_order_detail'),
    path('admin-portal/products/', admin_views.admin_products, name='admin_products'),
    path('admin-portal/products/add/', admin_views.admin_product_add, name='admin_product_add'),
    path('admin-portal/products/<int:product_id>/edit/', admin_views.admin_product_edit, name='admin_product_edit'),
    path('admin-portal/settings/', admin_views.admin_settings, name='admin_settings'),
    path('admin-portal/test-telegram/', admin_views.test_telegram_notification, name='test_telegram'),
    path('payment/upi-qr/', views_qr.upi_qr, name='upi_qr'),
    path('admin-portal/banners/', admin_views.admin_banners, name='admin_banners'),
    path('admin-portal/banners/add/', admin_views.admin_banner_add, name='admin_banner_add'),
    path('admin-portal/banners/<int:banner_id>/edit/', admin_views.admin_banner_edit, name='admin_banner_edit'),
    path('admin-portal/banners/<int:banner_id>/delete/', admin_views.admin_banner_delete, name='admin_banner_delete'),
    path('admin-portal/analytics/', admin_views.admin_analytics, name='admin_analytics'),
    
    # AJAX
    path('api/calculate-price/', views.calculate_price, name='calculate_price'),
    path('api/admin/update-order-status/', admin_views.admin_update_order_status, name='admin_update_order_status'),
]