"""
TechAi Samachar — SMTP Email Dispatcher
Delivers the vintage newspaper newsletter via SMTP with full anti-spam header compliance:
- Formatted Date header
- Unique Message-ID header
- Multipart alternative with plain-text fallback
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
from typing import List, Tuple
from config import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS, EMAIL_TO

def parse_recipients(to_str: str) -> List[str]:
    """Splits comma-separated recipient emails and cleans whitespace."""
    if not to_str:
        return []
    return [addr.strip() for addr in to_str.split(",") if addr.strip()]

def send_newspaper_email(
    html_content: str,
    subject: str,
    recipients: List[str] | None = None
) -> Tuple[bool, str]:
    """
    Dispatches the vintage newspaper HTML email via SMTP.
    Includes proper RFC-compliant headers (Date, Message-ID, Plain-text fallback)
    to ensure optimal inbox delivery and prevent spam filtering.
    """
    if not EMAIL_USER or not EMAIL_PASS:
        return False, "SMTP credentials missing: Please define EMAIL_USER and EMAIL_PASS in your .env file."

    target_recipients = recipients or parse_recipients(EMAIL_TO)
    if not target_recipients:
        return False, "No recipient addresses provided in EMAIL_TO."

    # 1. Create RFC-compliant MIME message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f'"TechAi Samachar" <{EMAIL_USER}>'
    msg["To"] = ", ".join(target_recipients)
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="gmail.com")
    msg["X-Mailer"] = "TechAi Samachar Vintage Dispatcher"

    # 2. Attach Plain-Text Fallback (Critical for anti-spam rating)
    plain_text = (
        f"{subject}\n\n"
        "TechAi Samachar — Your Daily AI & Technology Broadsheet Newspaper.\n\n"
        "Today's edition features curated updates on frontier AI reasoning, new phone & laptop launches, "
        "Nvidia & GPU silicon news, China tech developments, and upcoming conferences.\n\n"
        "Please view this email in an HTML-compatible email reader to view the full broadsheet layout."
    )
    part_text = MIMEText(plain_text, "plain", "utf-8")
    msg.attach(part_text)

    # 3. Attach Full HTML Payload
    part_html = MIMEText(html_content, "html", "utf-8")
    msg.attach(part_html)

    try:
        print(f"[SMTP Dispatcher] Connecting to {EMAIL_HOST}:{EMAIL_PORT}...")
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT, timeout=30)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, target_recipients, msg.as_string())
        server.quit()
        success_msg = f"Dispatched newsletter successfully to: {', '.join(target_recipients)}"
        print(f"[SMTP Dispatcher] ✅ {success_msg}")
        return True, success_msg

    except smtplib.SMTPAuthenticationError as auth_err:
        err_msg = (
            f"SMTP Authentication Failed: {auth_err}. "
            "Note: If using Gmail, you MUST generate and use a 16-character App Password, "
            "not your standard Google account password. Visit: https://myaccount.google.com/apppasswords"
        )
        print(f"[SMTP Dispatcher] ❌ {err_msg}")
        return False, err_msg
    except Exception as e:
        err_msg = f"Failed to send email via SMTP: {e}"
        print(f"[SMTP Dispatcher] ❌ {err_msg}")
        return False, err_msg

def test_smtp_connection() -> Tuple[bool, str]:
    """Tests connection and credentials against configured SMTP server."""
    if not EMAIL_USER or not EMAIL_PASS:
        return False, "EMAIL_USER or EMAIL_PASS is missing in .env"
    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT, timeout=15)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.quit()
        return True, "SMTP connection and credentials verified successfully."
    except Exception as e:
        return False, f"SMTP Test Failed: {e}"
