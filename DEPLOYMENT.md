# 🚀 Production Deployment Guide

This guide will help you deploy your Django resin art business website to production.

## 📋 Pre-Deployment Checklist

### 1. **Environment Variables**
Create a `.env` file in production (never commit this!):

```bash
# Django Settings
SECRET_KEY=your-super-secret-key-here-change-this
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (if using PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Telegram Notifications
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id

# Website URL
WEBSITE_URL=https://yourdomain.com
```

### 2. **Update settings.py for Production**

Add to `Business/settings.py`:

```python
import os
from pathlib import Path

# Security Settings
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_H