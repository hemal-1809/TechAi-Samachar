# 🗞️ TechAI Samachar (Vintage Newspaper AI Digest)

A vintage-styled, automated AI & tech news publication engine written in **Python**. It leverages **Gemini API** with **Google Search Grounding** (live web search) to curate the latest breakthroughs in artificial intelligence, silicon & GPU updates, mobile and laptop launches, China tech, and hackathons — outputting an authentic **vintage broadsheet newspaper** delivered via email and viewable online.

Inspired by classic boutique European editorial design (aged newsprint, Didone serif masthead, 3-column sub-tickers, duotone/monochrome lead photo, and "Sabias Que" editorial analysis).

---

## 📸 Key Design & Features

- **📰 Vintage Online Broadsheet Edition**:
  - Full aesthetic layout with warm parchment newsprint (`#F6F4EE`), authentic letterpress typography (`Playfair Display`, `EB Garamond`, `Cinzel`), and grain texture.
  - Interactive top toolbar with **Toggle Paper Tint (Sepia / Parchment)**, **Print Newspaper (PDF)**, and **Copy Email HTML**.
- **✉️ Cross-Client Vintage Email Output**:
  - Built with responsive HTML tables and inline CSS compatible with Gmail, Outlook, Apple Mail, and mobile inboxes.
  - 3-column top masthead with Japanese/Gujarati editorial badges and red volume stamps (`# 001`).
  - 3-column sub-headline ticker (`AI & FRONTIER`, `HARDWARE & SILICON`, `GLOBAL TECH`).
  - Lead story layout featuring monochrome hero photography.
  - Dual-column editorial grid with categorized updates and the **"Sabias Que..."** Editor's take.
  - Vintage classifieds calendar for events in the USA, India, Gujarat, and Hackathons.
  - Grounded source citations formatted as an antique academic bibliography.

---

## 📁 Project Structure

```
TechAi-Samachar/
├── main.py                  # Main CLI entry point
├── config.py                # Environment configuration & date/edition helpers
├── agent.py                 # Gemini API with Google Search Grounding & demo fallback
├── templates.py             # Vintage Email & Vintage Online HTML layout engines
├── mailer.py                # SMTP email dispatcher with TLS & App Password support
├── requirements.txt         # Python dependencies (google-genai, python-dotenv, requests)
├── .env.example             # Configuration template
├── vintage_online_output.html # Generated interactive vintage online webpage
├── vintage_email_output.html  # Generated inline-styled email template
└── .github/workflows/
    └── daily-email.yml      # Automated 8:30 AM IST GitHub Action runner
```

---

## 🚀 Quick Start (Local Setup)

### 1. Install Dependencies
Ensure you have Python 3.10+ installed:
```bash
pip install -r requirements.txt
```

### 2. Immediate Preview (No API Key Required)
Generate and preview the vintage online newspaper and email layouts right in your browser:
```bash
python main.py --demo
```
This generates:
- `vintage_online_output.html` (interactive vintage web broadsheet)
- `vintage_email_output.html` (email HTML preview)

You can double-click either file to view it in Chrome, Edge, or Safari!

---

## 🔑 Live Setup with Gemini & Email Delivery

### 1. Configure `.env`
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Fill in your credentials:
```env
# 1. Gemini API Key from https://aistudio.google.com/
GEMINI_API_KEY=AIzaSy...your-key-here

# 2. Gmail SMTP Credentials
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_sender_email@gmail.com
# IMPORTANT: Use a 16-character Gmail App Password (NOT your regular password)
EMAIL_PASS=abcd efgh ijkl mnop

# 3. Recipients (comma-separated for multiple inboxes)
EMAIL_TO=recipient1@gmail.com, recipient2@gmail.com

# 4. Optional Editorial Credits
EDITOR_NAME=Hemal Mistry
EDITOR_TITLE=Editor-in-Chief, TechAi Samachar
```

### 2. Test SMTP Connection
```bash
python main.py --test-smtp
```

### 3. Generate & Dispatch Live Edition
```bash
python main.py
```

### 4. Fetch Live News Without Sending Email
```bash
python main.py --no-email
```

---

## ☁️ Automated Daily Cloud Delivery (GitHub Actions)

This repository includes a GitHub Action workflow (`.github/workflows/daily-email.yml`) scheduled to execute every morning at **8:30 AM IST** (3:00 AM UTC).

1. Push this repository to GitHub (Private repository recommended).
2. Go to **Settings > Secrets and variables > Actions**.
3. Add the following repository secrets:
   - `GEMINI_API_KEY`
   - `EMAIL_USER`
   - `EMAIL_PASS`
   - `EMAIL_TO`
4. The workflow will run automatically every morning, or you can trigger it manually via **Actions > Run workflow**.

---

## 📜 License
MIT License. Created by Hemal Mistry.
