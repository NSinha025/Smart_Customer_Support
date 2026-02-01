# 🚀 Free Deployment Guide

This guide shows you how to deploy your Smart Customer Support application for **FREE** using various platforms.

## 📋 Prerequisites

Before deploying, make sure you have:
- A GitHub account
- Your OpenAI API key
- Git installed on your machine

## 🎯 Best Free Hosting Options

### Option 1: Render.com (Recommended ⭐)

**Pros:** Easy setup, free SSL, auto-deploy from GitHub, 750 hours/month free

**Steps:**

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

2. **Deploy on Render:**
   - Go to https://render.com and sign up
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name:** smart-customer-support
     - **Runtime:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn app:app`
   - Add Environment Variables:
     - `OPENAI_API_KEY` = your-api-key
     - `SECRET_KEY` = (generate a random string)
   - Click "Create Web Service"

3. **Your app will be live at:** `https://your-app-name.onrender.com`

---

### Option 2: Railway.app

**Pros:** Generous free tier, automatic deployments, easy database hosting

**Steps:**

1. **Push code to GitHub** (same as above)

2. **Deploy on Railway:**
   - Go to https://railway.app and sign up
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect Python and deploy
   - Add Environment Variables:
     - `OPENAI_API_KEY` = your-api-key
     - `SECRET_KEY` = random-string
   - Click "Deploy"

3. **Generate domain:** Click "Settings" → "Generate Domain"

---

### Option 3: PythonAnywhere

**Pros:** Python-focused, persistent storage, free custom domain

**Steps:**

1. **Sign up at:** https://www.pythonanywhere.com

2. **Upload your code:**
   - Use "Files" tab to upload your project
   - Or clone from GitHub using Bash console

3. **Install dependencies:**
   ```bash
   pip install --user -r requirements.txt
   ```

4. **Configure Web App:**
   - Go to "Web" tab → "Add a new web app"
   - Choose "Flask"
   - Point to your `app.py` file
   - Set environment variables in WSGI configuration file

5. **Your app will be at:** `https://yourusername.pythonanywhere.com`

---

### Option 4: Fly.io

**Pros:** Global edge deployment, free tier includes 3 VMs

**Steps:**

1. **Install Fly CLI:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Initialize and deploy:**
   ```bash
   fly launch
   fly secrets set OPENAI_API_KEY=your-key
   fly secrets set SECRET_KEY=random-string
   fly deploy
   ```

---

## 🔧 Configuration Files Included

Your project now includes deployment configs for multiple platforms:

- **`Procfile`** - For Render, Railway, Heroku
- **`render.yaml`** - For Render.com
- **`vercel.json`** - For Vercel (serverless)
- **`runtime.txt`** - Python version specification
- **`requirements.txt`** - Updated with `gunicorn`

## 🔐 Important: Environment Variables

**Never commit your `.env` file!** Make sure `.gitignore` includes:
```
.env
*.db
__pycache__/
venv/
```

Set these environment variables on your hosting platform:
- `OPENAI_API_KEY` - Your OpenAI API key
- `SECRET_KEY` - Random string for Flask sessions

## 📊 Free Tier Limits

| Platform | Free Tier | Best For |
|----------|-----------|----------|
| **Render** | 750 hrs/month, auto-sleep | Most projects |
| **Railway** | $5 credit/month | Databases included |
| **PythonAnywhere** | 1 web app | Python projects |
| **Fly.io** | 3 VMs, 160GB bandwidth | Global deployment |

## 🚀 Quick Deploy Commands

### For Render/Railway (Git-based):
```bash
# Commit and push
git add .
git commit -m "Ready for deployment"
git push origin main

# Then connect via their web dashboard
```

### For Fly.io (CLI-based):
```bash
fly launch
fly secrets set OPENAI_API_KEY=your-key
fly deploy
```

## 🐛 Troubleshooting

**App won't start?**
- Check logs on your platform dashboard
- Verify environment variables are set
- Ensure `gunicorn` is in `requirements.txt`

**Database not persisting?**
- Free tiers may have ephemeral storage
- Consider using a managed database service

**API key not working?**
- Double-check the environment variable name
- Ensure no extra spaces or quotes

## 📝 Post-Deployment

After deployment:
1. Test all endpoints
2. Check `/health` endpoint
3. Try sample queries
4. Monitor logs for errors

## 🎉 You're Live!

Your Smart Customer Support app is now accessible worldwide! Share your deployment URL with users.

**Need help?** Check the platform-specific documentation:
- [Render Docs](https://render.com/docs)
- [Railway Docs](https://docs.railway.app)
- [PythonAnywhere Help](https://help.pythonanywhere.com)
- [Fly.io Docs](https://fly.io/docs)
