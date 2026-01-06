#!/usr/bin/env python3
"""
Quick test script for Telegram notifications
Run this to test your Telegram bot setup
"""

import requests

# Replace these with your actual values
BOT_TOKEN = "8396259140:AAGUL7thJQhVYMScyzpuI9gzSr1QBj3xdw8"  # From @BotFather
CHAT_ID = "2123056460"      # From @userinfobot

def test_telegram():
    """Test sending a message via Telegram"""
    
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or CHAT_ID == "YOUR_CHAT_ID_HERE":
        print("❌ Please edit this file and add your BOT_TOKEN and CHAT_ID")
        return
    
    print("🔄 Testing Telegram notification...")
    print(f"Bot Token: {BOT_TOKEN[:10]}...")
    print(f"Chat ID: {CHAT_ID}")
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    message = """
🧪 <b>Test Notification</b>

✅ If you see this message, your Telegram bot is working correctly!

You can now receive order notifications on your phone.
"""
    
    data = {
        'chat_id': CHAT_ID,
        'text': message.strip(),
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, data=data, timeout=10)
        
        if response.status_code == 200:
            print("✅ SUCCESS! Check your Telegram - you should have received a test message!")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ FAILED! Status code: {response.status_code}")
            print(f"Response: {response.text}")
            
            # Common error messages
            if "Unauthorized" in response.text:
                print("\n💡 TIP: Your Bot Token is incorrect. Get it from @BotFather")
            elif "chat not found" in response.text:
                print("\n💡 TIP: Your Chat ID is incorrect or you haven't started the bot yet.")
                print("   1. Search for your bot on Telegram")
                print("   2. Click 'Start' or send /start")
                print("   3. Try again")
            elif "Bad Request" in response.text:
                print("\n💡 TIP: Check that your Chat ID is just numbers (no letters)")
                
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        print("\n💡 TIP: Check your internet connection")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_telegram()
