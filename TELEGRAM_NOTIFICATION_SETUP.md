# 📱 Telegram Notification Setup Guide

Get instant notifications on your phone when customers place orders!

## 🚀 Quick Setup (5 minutes)

### Step 1: Create a Telegram Bot

1. Open **Telegram** on your phone
2. Search for **@BotFather** (official Telegram bot)
3. Start a chat and send: `/newbot`
4. Follow the prompts:
   - Choose a name for your bot (e.g., "My Business Orders")
   - Choose a username (must end with 'bot', e.g., "mybusiness_orders_bot")
5. **Copy the Bot Token** - it looks like this:
   ```
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

### Step 2: Get Your Chat ID

1. Search for **@userinfobot** on Telegram
2. Start a chat and send any message
3. The bot will reply with your user info
4. **Copy your Chat ID** - it's a number like: `123456789`

### Step 3: Start Your Bot

1. Search for your bot (the username you created in Step 1)
2. Click **"Start"** or send `/start`
3. This allows your bot to send you messages

### Step 4: Configure in Admin Panel

1. Go to your **Admin Portal** → **Settings**
2. Scroll to **"Order Notifications (Telegram)"** section
3. Paste your **Bot Token**
4. Paste your **Chat ID**
5. Toggle **"Enable Telegram Notifications"** to ON
6. Click **"Save All Settings"**

### Step 5: Test It!

1. Place a test order on your website
2. You should receive an instant notification on Telegram! 🎉

## 📋 What You'll Receive

When a customer places an order, you'll get a message like:

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

✅ Payment proof uploaded
```

## 🔧 Troubleshooting

### Not receiving notifications?

1. **Check if bot is started**: Search for your bot and click "Start"
2. **Verify credentials**: Make sure Bot Token and Chat ID are correct
3. **Check toggle**: Ensure "Enable Telegram Notifications" is ON
4. **Test the bot**: Send a message to your bot to confirm it's active

### Wrong Chat ID?

- Make sure you're using YOUR Chat ID (from @userinfobot)
- Don't use the bot's ID or username

### Bot Token expired?

- Contact @BotFather and use `/token` to regenerate
- Update the new token in settings

## 🔒 Security Notes

- Keep your Bot Token private (like a password)
- Only you will receive notifications (using your Chat ID)
- The bot can only send messages, not read your chats

## 💡 Pro Tips

1. **Multiple Admins**: Each admin can create their own bot and add their Chat ID
2. **Mute Notifications**: Use Telegram's mute feature during off-hours
3. **Archive Orders**: Keep your Telegram chat organized by archiving old notifications

## 📞 Need Help?

If you have issues:
1. Verify all steps were followed correctly
2. Check that Django server is running
3. Look for error messages in server logs
4. Make sure `requests` library is installed: `pip install requests`

---

## 🎯 Alternative: WhatsApp Notifications

If you prefer WhatsApp, you can use:
- **Twilio WhatsApp API** (paid, but reliable)
- **WhatsApp Business API** (requires approval)

Let me know if you'd like help setting up WhatsApp instead!
