"""
TechAi Samachar — Daily Vintage Newspaper Agent & Email Dispatcher
Main Entry Point
"""

import argparse
import os
import sys
from config import (
    GEMINI_API_KEY,
    EMAIL_USER,
    EMAIL_PASS,
    EMAIL_TO,
    get_formatted_date,
    get_short_date,
    get_edition_number,
)
from agent import fetch_and_curate_news, get_demo_html
from templates import build_vintage_email_html, build_vintage_web_html
from mailer import send_newspaper_email, test_smtp_connection

def parse_args():
    parser = argparse.ArgumentParser(
        description="TechAi Samachar — Vintage Daily Tech Newspaper Generator & Emailer"
    )
    parser.add_argument(
        "--demo", "--preview",
        action="store_true",
        help="Generate preview outputs using curated demo data without requiring API keys or SMTP."
    )
    parser.add_argument(
        "--no-email",
        action="store_true",
        help="Generate vintage web and email outputs without attempting to send email."
    )
    parser.add_argument(
        "--test-smtp",
        action="store_true",
        help="Test connection to SMTP server using configured credentials."
    )
    parser.add_argument(
        "--web-output",
        default="vintage_online_output.html",
        help="Path for generated vintage online webpage (default: vintage_online_output.html)."
    )
    parser.add_argument(
        "--email-output",
        default="vintage_email_output.html",
        help="Path for generated vintage email HTML (default: vintage_email_output.html)."
    )
    return parser.parse_args()


def main():
    args = parse_args()

    print("=" * 72)
    print(" 🗞️  TECHAI SAMACHAR — VINTAGE NEWSPAPER PUBLICATION ENGINE")
    print("=" * 72)

    # 1. Test SMTP if requested
    if args.test_smtp:
        print("[Status] Testing SMTP connection...")
        ok, msg = test_smtp_connection()
        print(f"[{'SUCCESS' if ok else 'FAILURE'}] {msg}")
        sys.exit(0 if ok else 1)

    today = get_formatted_date()
    short_date = get_short_date()
    edition = get_edition_number()

    print(f"Target Edition: #{edition:03d} | Date: {today}")

    # 2. Fetch or Generate News Data (9 comprehensive sections)
    if args.demo:
        print("[Mode] Running in PREVIEW / DEMO mode with curated 9-section vintage edition.")
        body_html = get_demo_html()
        citations = [
            {"title": "Google DeepMind Frontier Intelligence", "url": "https://deepmind.google"},
            {"title": "Nvidia Blackwell Datacenter Silicon", "url": "https://www.nvidia.com"},
            {"title": "Smart India Hackathon 2026", "url": "https://www.sih.gov.in"},
            {"title": "GIFT City FinTech Gujarat Hub", "url": "https://giftgujarat.in"},
        ]
    else:
        print("[Mode] Dispatching 9-section news curation agent with Google Search Grounding...")
        body_html, citations = fetch_and_curate_news()

    # 3. Build Layouts
    print("[Layout Engine] Rendering Vintage Newspaper Email HTML (table-based, inline CSS)...")
    email_html = build_vintage_email_html(body_html, citations, today, short_date, edition)

    print("[Layout Engine] Rendering Vintage Online Webpage (custom fonts, grain texture, reader mode)...")
    web_html = build_vintage_web_html(email_html, short_date, edition)

    # 4. Save HTML Artifacts
    try:
        with open(args.email_output, "w", encoding="utf-8") as f:
            f.write(email_html)
        print(f"[File Output] Saved Vintage Email HTML -> {os.path.abspath(args.email_output)}")

        with open(args.web_output, "w", encoding="utf-8") as f:
            f.write(web_html)
        print(f"[File Output] Saved Vintage Online Webpage -> {os.path.abspath(args.web_output)}")
    except Exception as e:
        print(f"[Warning] Could not write output files: {e}")

    # 5. Send Email
    if args.no_email or args.demo:
        print("\n[Complete] Skipped email delivery as requested. You can view the generated files in your browser:")
        print(f" 👉 Vintage Online Web:  {os.path.abspath(args.web_output)}")
        print(f" 👉 Vintage Email View:  {os.path.abspath(args.email_output)}")
        return

    if not EMAIL_USER or not EMAIL_PASS or not EMAIL_TO:
        print("\n[Notice] SMTP credentials not detected in .env.")
        print("To send automatically via email, configure in your .env file:")
        print("  GEMINI_API_KEY=your_gemini_api_key")
        print("  EMAIL_USER=your_gmail@gmail.com")
        print("  EMAIL_PASS=your_16_char_gmail_app_password")
        print("  EMAIL_TO=recipient@example.com")
        print(f"\nYour vintage newspaper files are ready to view locally:")
        print(f" 👉 Vintage Online Web:  {os.path.abspath(args.web_output)}")
        print(f" 👉 Vintage Email View:  {os.path.abspath(args.email_output)}")
        return

    subject = f"🗞️ TechAi Samachar — {short_date} — Issue #{edition:03d} · 9 Daily Dispatches"
    print(f"\n[SMTP Dispatcher] Sending vintage email edition to: {EMAIL_TO}...")
    success, msg = send_newspaper_email(email_html, subject)

    if success:
        print(f"[Complete] ✅ {msg}")
    else:
        print(f"[Attention] {msg}")

if __name__ == "__main__":
    main()
