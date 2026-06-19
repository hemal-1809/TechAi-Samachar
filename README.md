# 🔥 TechAI Samchar (Daily AI & Tech News Agent)

A fully automated, comprehensive AI-powered tech news agent that searches the internet for the latest AI breakthroughs, phone and laptop launches, GPU news, China tech moves, Big Tech updates, events, and more — then compiles everything into a **stunning, premium HTML email** and delivers it straight to your inbox every morning at **8:30 AM IST**.

> Powered by **Gemini 2.5 Flash** with **Google Search Grounding** (live internet search) + **Nodemailer**.

---

## 📸 What You Get

Every morning you receive a beautifully designed email with **9 curated sections**:
- 🚨 **Breaking News** : The single biggest tech headline with "Why This Matters" analysis
- 🤖 **AI Models & Tools** : OpenAI, Google, Anthropic, Meta, Mistral, xAI, Midjourney, and more
- 📱 **Mobile Phones** : New launches and updates from Apple, Samsung, Xiaomi, OnePlus, Realme, and more (India prices included)
- 💻 **Laptops** : MacBook, ThinkPad, ROG, XPS, Surface launches with specs and India pricing
- 🎮 **Nvidia & GPU News** : RTX updates, AI chips, CUDA, Nvidia earnings and announcements
- 🇨🇳 **China Tech** : Huawei, DeepSeek, Baidu, Alibaba, ByteDance, BYD, DJI updates
- 🏢 **Big Tech** : Apple, Google, Microsoft, Meta, Amazon, Tesla, SpaceX Starlink news
- 📅 **Events & Conferences** : USA, India, Gujarat-specific events, and college hackathons
- ✍️ **Editor's Take** : Personal commentary with a motivational line for Indian tech students
- 📎 **Sources & References** : Every source article, clickable and numbered

**Every headline is clickable** and takes you directly to the original article!
News is tagged with 🇮🇳 (India) or 🌍 (Global) flags, plus 🆕 NEW LAUNCH and 🤖 NEW MODEL badges.

---

## 🛠️ Table of Contents

1. [Get a Free Gemini API Key](#1-get-a-free-gemini-api-key)
2. [Get a Gmail App Password](#2-get-a-gmail-app-password)
3. [Local Setup & Testing](#3-local-setup--testing)
4. [Deploy to Cloud with GitHub Actions (Free)](#4-deploy-to-cloud-with-github-actions-free)
5. [Local Scheduling with Windows Task Scheduler](#5-local-scheduling-with-windows-task-scheduler)

---

## 1. Get a Free Gemini API Key

1. Go to **[Google AI Studio](https://aistudio.google.com/)**.
2. Log in with your Google Account.
3. Click **"Get API Key"** in the left sidebar.
4. Click **"Create API Key"** → Select or create a Google Cloud Project.
5. **Copy the key** — it starts with `Abc..123..Xyz...`.

---

## 2. Get a Gmail App Password

Standard Gmail passwords are blocked by Google for script access. You need an **App Password**:

1. Go to **[Google Account → Security](https://myaccount.google.com/security)**.
2. Enable **2-Step Verification** if not already active.
3. Search for **"App passwords"** in the search bar at the top.
4. Enter a name (e.g., `TechAI Samchar`) → Click **Create**.
5. **Copy the 16-character code** shown (e.g., `abcd efgh ijkl mnop`).

---

## 3. Local Setup & Testing

### Step 1: Fill in your `.env` file

Open the `.env` file in the project root and add your credentials:

```env
GEMINI_API_KEY=AIzaSy...your-key-here
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-gmail@gmail.com
EMAIL_PASS=abcdefghijklmnop
EMAIL_TO=recipient1@gmail.com, recipient2@gmail.com
```

> 💡 **Multiple recipients?** Just add more emails separated by commas!

### Step 2: Install dependencies

```bash
npm install
```

### Step 3: Run it!

```bash
npm start
```

Check your inbox — you should see a stunning **TechAI Samchar** newsletter!

---

## 4. Deploy to Cloud with GitHub Actions (Free)

This is the **recommended** approach. It runs automatically every morning at 8:30 AM IST in the cloud — **your PC doesn't need to be on!**

### Step 1: Create a Private GitHub Repo
1. Go to [github.com/new](https://github.com/new)
2. Name it (e.g., `techai-samchar`)
3. Set to **Private** → Click **Create Repository**

### Step 2: Add Secrets
In your repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**:

| Secret Name      | Value                          |
|------------------|--------------------------------|
| `GEMINI_API_KEY` | Your Gemini API key            |
| `EMAIL_USER`     | Your sender Gmail address      |
| `EMAIL_PASS`     | Your 16-char Gmail App Password|
| `EMAIL_TO`       | Recipient email(s), comma-separated |

### Step 3: Push the Code
```bash
git init
git add .
git commit -m "feat: launch TechAI Samchar"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 4: Test it
1. Go to your repo → **Actions** tab
2. Click **TechAI Samchar—Daily Digest** on the left
3. Click **Run workflow** → **Run workflow** button
4. ✅ Done! It will also auto-run every day at 8:30 AM IST.

---

## 5. Local Scheduling with Windows Task Scheduler

If you prefer running it locally:

### Create `run_agent.bat`:
```cmd
@echo off
cd /d "C:\Users\HEMAL\Desktop\Portfolio"
node index.js >> agent_log.txt 2>&1
```

### Configure Windows Task Scheduler:
1. Open **Task Scheduler** (search in Start menu)
2. Click **Create Basic Task**
3. Name: `TechAI Samchar`
4. Trigger: **Daily** at **8:30 AM**
5. Action: **Start a program** → Browse to `run_agent.bat`
6. Start in: `C:\Users\HEMAL\Desktop\Portfolio`
7. Click **Finish**

---

## 📁 Project Structure

```
├── .github/workflows/
│   └── daily-email.yml         # Cloud scheduler (GitHub Actions)
├── .env                        # Your API keys (gitignored)
├── .env.example                # Template for credentials
├── .gitignore                  # Protects secrets from git
├── package.json                # Dependencies
├── index.js                    # Core TechAI Samchar engine
└── README.md                   # This guide
```

---

-Hemal Mistry
