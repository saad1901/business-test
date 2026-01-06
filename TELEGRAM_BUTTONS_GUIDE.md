# 📱 Enhanced Telegram Notifications with Buttons

Your Telegram notifications now include interactive buttons! 🎉

## 🎯 What's New?

When you receive an order notification, you'll now see:

### 📋 Order Information
- Customer name, phone, email
- Order items and total amount
- Delivery address
- Order time
- Payment screenshot link (clickable in message)

### 🔘 Interactive Buttons

**1. 📞 Call Customer**
   - Instantly call the customer's phone number
   - Opens your phone's dialer

**2. 💬 WhatsApp**
   - Opens WhatsApp chat with the customer
   - Pre-filled with their number

**3. 🔍 View Order Details**
   - Opens the order detail page in your admin panel
   - See full order information and manage status

**4. 💳 View Payment Screenshot**
   - Opens the payment proof image
   - Verify payment instantly

---

## 🚀 Setup Steps

### 1. Run Migrations
```bash
python manage.py migrate
```

### 2. Configure Website URL
1. Go to **Admin Portal → Settings**
2. Find **"Website URL"** field
3. Enter your website URL:
   - For production: `https://yoursite.com`
   - For local testing: `http://localhost:8000`
   - For ngrok: `https://your-ngrok-url.ngrok.io`
4. Save settings

### 3. Test It!
Place a test order and check your Telegram notification!

---

## 📱 Example Notification

```
🔔 New Order Received!

📦 Order ID: abc123-def456

👤 Customer:
John Doe
📱 9876543210
📧 john@example.com

🛍️ Items:
• Custom Keychain x2 - ₹500

💰 Total Amount: ₹500

📍 Delivery Address:
123 Main Street, City, 123456

⏰ Order Time: 06 Jan 2026, 03:30 PM

💳 View Payment Screenshot

[📞 Call Customer] [💬 WhatsApp]
[🔍 View Order Details]
[💳 View Payment Screenshot]
```

---

## 🔧 Troubleshooting

### Buttons not showing?
- Make sure you ran migrations: `python manage.py migrate`
- Restart Django server
- Place a new order to test

### Links not working?
- Check that **Website URL** is set correctly in settings
- For local testing, use `http://localhost:8000`
- For production, use your actual domain with `https://`

### Payment screenshot link not working?
- Make sure `MEDIA_URL` and `MEDIA_ROOT` are configured in settings.py
- Check that payment proof was uploaded successfully

---

## 💡 Pro Tips

1. **Use ngrok for local testing:**
   ```bash
   ngrok http 8000
   ```
   Then use the ngrok URL as your Website URL

2. **Quick Actions:**
   - Tap "Call" to instantly contact customer
   - Tap "WhatsApp" for quick messaging
   - Tap "View Order" to manage order status

3. **Payment Verification:**
   - Click payment screenshot link
   - Verify payment details
   - Update order status from admin panel

---

## 🎨 Customization

Want to add more buttons? Edit `app/utils.py` in the `send_telegram_notification_with_buttons` function!

Example buttons you could add:
- Email customer
- View customer's previous orders
- Mark as confirmed
- Generate invoice

---

## 🔒 Security Note

The buttons use your website's URLs. Make sure:
- Your admin panel requires authentication
- Payment screenshots are served securely
- Only authorized users can access admin URLs

---

Enjoy your enhanced notifications! 🚀
