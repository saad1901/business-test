from django.core.management.base import BaseCommand
from django.core.management import call_command
from app.models import Product, ProductImage, WebsiteSettings, Banner
import os


class Command(BaseCommand):
    help = 'Setup sample data for the resin art website'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up sample data...'))
        
        # Load sample products
        try:
            call_command('loaddata', 'sample_products.json')
            self.stdout.write(self.style.SUCCESS('✓ Sample products loaded'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading products: {e}'))
        
        # Create sample product images (placeholder)
        products = Product.objects.all()
        for product in products:
            if not product.images.exists():
                # Create placeholder image entries
                ProductImage.objects.create(
                    product=product,
                    image='products/placeholder.jpg',  # You can add actual images later
                    alt_text=f'{product.name} image',
                    is_primary=True,
                    order=0
                )
        
        self.stdout.write(self.style.SUCCESS('✓ Sample product images created'))
        
        # Create website settings
        if not WebsiteSettings.objects.exists():
            WebsiteSettings.objects.create(
                site_name='Custom Resin Art',
                tagline='Beautiful Personalized Resin Keychains & Gifts',
                contact_phone='+91 9876543210',
                contact_email='info@customresinart.com',
                upi_id='resinart@paytm',
                whatsapp_number='+91 9876543210',
                address='Mumbai, Maharashtra, India',
                processing_time_days=3,
                delivery_time_days=7
            )
            self.stdout.write(self.style.SUCCESS('✓ Website settings created'))
        
        # Create sample banners (you'll need to add actual images)
        if not Banner.objects.exists():
            Banner.objects.create(
                title='Beautiful Custom Resin Art',
                subtitle='Transform your memories into stunning keychains and gifts',
                banner_type='hero',
                image='banners/hero-banner.jpg',  # Add actual image
                link_url='/products/',
                link_text='Shop Now',
                is_active=True,
                order=1
            )
            self.stdout.write(self.style.SUCCESS('✓ Sample banner created'))
        
        self.stdout.write(
            self.style.SUCCESS(
                '\n🎉 Sample data setup complete!\n'
                'Next steps:\n'
                '1. Run: python manage.py runserver\n'
                '2. Visit /admin/ to manage products, orders, and settings\n'
                '3. Add real product images in media/products/\n'
                '4. Add banner images in media/banners/\n'
                '5. Update website settings in admin panel\n'
                '6. Test order tracking with mobile numbers\n'
            )
        )