# 🔧 Telegram Notification Troubleshooting

Not receiving notifications? Follow these steps:

## ✅ Step-by-Step Checklist

### 1. **Verify Bot Token**
- Go to Telegram and search for `@BotFather`
- Send `/mybots`
- Select your bot
- Click "API Token" to see your token
- It should look like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`
- Copy and paste it EXACTLY (no spaces)

### 2. **Verify Chat ID**
- Search for `@userinfobot` on Telegram
- Send any message
- Copy the **Id** number (NOT the username)
- It's just numbers, like: `123456789` or `-123456789`

### 3. **Start Your Bot** ⚠️ IMPORTANT!
This is the most common issue!
- Search for your bot on Telegram (use the username you created)
- Click **"START"** button or send `/start`
- You should see a welcome message
- **Without this step, the bot CANNOT send you messages!**

### 4. **Enable Notifications in Settings**
- Go to Admin Portal → Settings
- Scroll to "Order Notifications (Telegram)"
- Make sure the toggle is **ON** (blue/green)
- Click "Save All Settings"

### 5. **Test the Setup**
- In the same settings page, click **"Send Test Notification"**
- Check your Telegram immediately
- If you receive a test message ✅ = Working!
- If not, see common errors below

---

## 🐛 Common Errors & Solutions

### Error: "Unauthorized"
**Problem:** Bot Token is incorrect

**Solution:**
1. Go to @BotFather
2. Send `/mybots` → Select your bot → API Token
3. Copy the ENTIRE token (including the colon `:`)
4. Paste in settings and save

---

### Error: "Chat not found" or "Forbidden"
**Problem:** You haven't started the bot

**Solution:**
1. Search for your bot on Telegram
2. Click **"START"** or send `/start`
3. Try the test notification again

---

### Error: "Bad Request: chat_id is empty"
**Problem:** Chat ID is missing or incorrect

**Solution:**
1. Go to @userinfobot
2. Send any message
3. Copy ONLY the number after "Id:"
4. Paste in settings (no spaces, no letters)

---

### No Error, But No Notification
**Problem:** Settings not saved or toggle is off

**Solution:**
1. Check that "Enable Telegram Notifications" toggle is ON
2. Click "Save All Settings" button
3. Refresh the page to confirm settings are saved
4. Try test notification again

---

## 🧪 Manual Test (Advanced)

If the test button doesn't work, try this Python script:

```python
import requests

BOT_TOKEN = "YOUR_BOT_TOKEN"  # Replace with your token
CHAT_ID = "YOUR_CHAT_ID"      # Replace with your chat ID

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
data = {
    'chat_id': CHAT_ID,
    'text': 'Test message from Python!'
}

response = requests.post(url, data=data)
print(response.json())
```

Run it:
```bash
python3 test_telegram.py
```

---

## 📋 Quick Verification Checklist

- [ ] Bot Token is correct (from @BotFather)
- [ ] Chat ID is correct (from @userinfobot)
- [ ] I clicked "START" on my bot
- [ ] Toggle is ON in settings
- [ ] Settings are saved
- [ ] Test notification sent successfully
- [ ] `requests` library is installed (`pip install requests`)

---

## 🔍 Check Server Logs

If nothing works, check your Django server console for errors:

```bash
# Look for lines like:
Telegram notification error: ...
Notification error: ...
```

Common log errors:
- `Connection refused` → Internet/firewall issue
- `Module not found: requests` → Run `pip install requests`
- `Unauthorized` → Wrong bot token
- `Chat not found` → Haven't started bot

---

## 💡 Still Not Working?

1. **Restart Django server** after saving settings
2. **Check internet connection** - bot needs to reach Telegram API
3. **Try a different bot** - create a new one with @BotFather
4. **Check firewall** - make sure outgoing HTTPS is allowed
5. **Verify requests library**: `pip list | grep requests`

---

## ✅ Success Indicators

You'll know it's working when:
1. Test notification arrives on Telegram ✅
2. When you place an order, you get instant notification ✅
3. Notification includes order details ✅

---

## 📞 Need More Help?

Share these details:
- Error message from test button
- Server console logs
- Bot Token format (first 10 characters only)
- Whether you clicked "START" on the bot

---

## 🎯 Alternative: Use the Test Script

I've created `test_telegram.py` in your project root.

1. Edit the file and add your Bot Token and Chat ID
2. Run: `python3 test_telegram.py`
3. Check the output for specific errors

This will help identify the exact issue!
