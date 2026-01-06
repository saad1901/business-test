# Custom Resin Art Business Website

A Django-based e-commerce website for a custom resin art business that sells personalized keychains, photo resin products, and custom gifts. Features a mobile-friendly admin interface and guest order tracking system.

## 🌟 Key Features

### User-Facing Features
- **Landing Page**: Dynamic banner system with featured products
- **Product Catalog**: Browse all available resin art products
- **Custom Orders**: Complete order flow with customization (text/photo/both)
- **UPI Payment System**: QR code-based payment with screenshot verification
- **Order Tracking**: Track orders using mobile number or email (no login required)
- **Guest Checkout**: No mandatory registration required
- **Mobile-First Design**: Fully responsive for Indian mobile users

### Admin Features (Mobile-Friendly)
- **Order Management**: View, verify payments, and update order status
- **Payment Verification**: Review payment screenshots and confirm orders
- **Product Management**: Add/edit products with multiple images
- **Website Settings**: Update contact info, UPI details, processing times
- **Banner Management**: Manage homepage banners and promotional content
- **Customer Management**: View customer details and order history

### Technical Features
- **Django 5.2.6**: Latest stable Django version
- **Mobile Admin UI**: Responsive admin interface for phone management
- **Order Tracking System**: No-login order tracking with mobile/email
- **Dynamic Content**: Database-driven banners and settings
- **Image Handling**: Proper media file management
- **Indian Localization**: ₹ pricing, Indian timezone, UPI payments

## 📱 Mobile Admin Interface

The admin interface is optimized for mobile devices, allowing you to:
- View and manage orders on your phone
- Update order status with one tap
- View payment screenshots in full resolution
- Manage website settings and banners
- Responsive tables and forms for mobile use

## 🔍 Order Tracking System

Customers can track their orders without creating accounts:
1. Visit "Track Order" in the navigation
2. Enter mobile number or email used during order
3. View all orders with real-time status updates
4. See order progress with visual indicators

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Navigate to project directory**
   ```bash
   cd Business/
   ```

2. **Install dependencies**
   ```bash
   pip install django pillow
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create admin user**
   ```bash
   python manage.py createsuperuser
   ```

5. **Load sample data**
   ```bash
   python manage.py setup_sample_data
   ```

6. **Start the server**
   ```bash
   python manage.py runserver
   ```

7. **Access the website**
   - Main website: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/
   - Order tracking: http://127.0.0.1:8000/track-order/

## 📊 Admin Panel Guide

### Managing Orders
1. Go to `/admin/` and login
2. Click "Orders" to see all orders
3. Use filters to find specific orders
4. Click on any order to view details
5. Update status directly from the list view
6. View payment screenshots and customer details

### Website Settings
1. Go to "Website Settings" in admin
2. Update contact information
3. Set UPI payment details
4. Configure processing and delivery times
5. Add social media links

### Banner Management
1. Go to "Banners" in admin
2. Add new banners with images
3. Set banner type (Hero, Promotion, Announcement)
4. Configure display order
5. Add optional links and button text

### Order Status Management
- **Payment Verification Pending**: New orders waiting for payment verification
- **Order Confirmed**: Payment verified, order confirmed
- **In Progress**: Order is being crafted
- **Completed**: Order finished and delivered
- **Cancelled**: Order cancelled

## 📱 Mobile Admin Usage

### On Your Phone:
1. Open browser and go to your-domain.com/admin/
2. Login with admin credentials
3. Navigate easily with mobile-optimized interface
4. Tap on orders to view details
5. Update order status with dropdown
6. View payment screenshots by tapping
7. Manage products and settings

### Order Verification Workflow:
1. Customer places order and uploads payment proof
2. You receive notification (if configured)
3. Open admin on phone
4. Go to Orders section
5. Find pending payment orders
6. Tap to view payment screenshot
7. Verify payment and update status to "Confirmed"
8. Customer can track updated status

## 🔧 Configuration

### UPI Payment Settings
Update in Admin → Website Settings:
- UPI ID: your-upi-id@bank
- Contact Phone: +91 XXXXXXXXXX
- WhatsApp Number: +91 XXXXXXXXXX

### Adding Product Images
1. Go to Admin → Products
2. Click on a product
3. Scroll to "Product images" section
4. Add multiple images
5. Set one as primary image

### Banner Management
1. Go to Admin → Banners
2. Add new banner
3. Upload banner image
4. Set title and subtitle
5. Configure link URL and button text
6. Set display order

## 🎯 Customer Journey

### Placing an Order:
1. Browse products
2. Select product and customize
3. Enter delivery details
4. Make UPI payment
5. Upload payment screenshot
6. Receive order confirmation

### Tracking Order:
1. Click "Track Order" in menu
2. Enter mobile number or email
3. View order status and progress
4. See estimated delivery time
5. Contact support if needed

## 📋 Order Status Flow

```
Order Placed → Payment Verification Pending → Order Confirmed → In Progress → Completed
```

Each status shows different information to customers:
- **Pending**: Waiting for payment verification
- **Confirmed**: Payment verified, production starting
- **In Progress**: Item being crafted
- **Completed**: Order delivered

## 🛠️ Customization

### Adding New Features
- SMS notifications for order updates
- Email confirmations
- Inventory management
- Discount codes
- Customer reviews
- Bulk order management

### Styling Changes
- Edit `static/css/style.css`
- Modify templates in `templates/`
- Update admin CSS in `static/admin/css/mobile-admin.css`

## 📞 Support Features

### Customer Support Integration
- WhatsApp integration for quick support
- Phone number display
- Order tracking reduces support queries
- Payment screenshot verification

### Admin Notifications
- Visual indicators for pending orders
- Payment status badges
- Order count displays
- Mobile-friendly alerts

## 🔒 Security Features

- CSRF protection enabled
- File upload validation
- User input sanitization
- Secure payment proof handling
- Admin access restrictions

## 📈 Business Benefits

### For Business Owner:
- Manage orders from anywhere using phone
- Quick payment verification
- Reduced customer support queries
- Professional order tracking system
- Easy content management

### For Customers:
- No account creation required
- Easy order tracking
- Transparent order status
- Mobile-friendly experience
- Secure payment process

## 🚀 Production Deployment

### Before Going Live:
1. Set `DEBUG = False` in settings.py
2. Add your domain to `ALLOWED_HOSTS`
3. Configure proper database (PostgreSQL)
4. Set up static file serving
5. Configure HTTPS
6. Set up backup system
7. Configure email notifications

### Recommended Hosting:
- DigitalOcean App Platform
- Heroku
- Railway
- PythonAnywhere

## 📝 License

This project is created for small business use. Customize as needed for your resin art business.

---

**🎉 Your resin art business website is ready!** 

The system is designed to work without customer accounts - they can track orders using just their mobile number or email. The mobile-friendly admin lets you manage everything from your phone, making it perfect for small business owners who are always on the go.