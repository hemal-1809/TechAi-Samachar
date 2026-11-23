"""
TechAi Samachar — Vintage Newspaper Template Engine
Combines the authentic vintage broadsheet editorial masthead (from reference image)
with the 9 comprehensive tech sections, fully optimized for mobile phone screens
and desktop email clients with a 100% cohesive vintage newspaper aesthetic.
"""

from typing import Any, Dict, List
import html
import re
from config import EDITOR_NAME, EDITOR_TITLE

def escape(val: Any) -> str:
    """Safe HTML escaping."""
    if val is None:
        return ""
    return html.escape(str(val))


def sanitize_to_vintage_theme(body_html: str) -> str:
    """
    Enforces a strict, cohesive vintage broadsheet aesthetic across the entire email body:
    - Upgrades all section headers to dark, high-contrast letterpress ribbons (#0a0a0a) with crisp white serif titles and red stamp tags.
    - Neutralizes bright modern SaaS colors (neon purples, blues, pinks, limes) to vintage black, ivory, and letterpress red.
    - Replaces rounded modern buttons with classic vintage boxed letterpress buttons.
    - Replaces modern card styles with crisp newspaper print compartments.
    - Enforces mobile responsiveness (fluid widths, word-break).
    """
    s = body_html

    # Strip section signs (&sect; or §) from anywhere in headers or text
    s = re.sub(r'(&sect;|§)\s*', '', s)

    # 1. Standardize and darken ANY section header variants into solid dark letterpress ribbons
    # Transform old h2 section headers
    def replace_h2(match):
        header_text = match.group(1)
        # Strip internal tags or emojis for clean vintage title
        clean_title = re.sub(r'<[^>]+>', ' ', header_text)
        # Remove emojis and section signs
        clean_title = re.sub(r'[\U00010000-\U0010ffff]|[\u2600-\u27bf]', '', clean_title)
        clean_title = re.sub(r'(&sect;|§)', '', clean_title).strip()
        clean_title = re.sub(r'\s+', ' ', clean_title)
        
        # Decide badge label
        badge = "DISPATCH"
        upper_title = clean_title.upper()
        if "BREAKING" in upper_title:
            badge = "WIRE"
        elif "PHONE" in upper_title or "MOBILE" in upper_title:
            badge = "TELEPHONY"
        elif "LAPTOP" in upper_title:
            badge = "SILICON"
        elif "GPU" in upper_title or "NVIDIA" in upper_title:
            badge = "SILICON"
        elif "CHINA" in upper_title:
            badge = "DOSSIER"
        elif "BIG TECH" in upper_title or "COMPANY" in upper_title:
            badge = "ENTERPRISE"
        elif "EVENT" in upper_title or "CONFERENCE" in upper_title:
            badge = "UPCOMING"
        elif "EDITOR" in upper_title or "SABIAS" in upper_title or "DID YOU KNOW" in upper_title:
            badge = "OPINION"

        return f'''<div style="background:#0a0a0a; border:1px solid #000000; padding:10px 14px; margin:34px 0 16px 0;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
      <td align="left" style="font-family:'Playfair Display',Georgia,'Times New Roman',serif; font-size:14px; font-weight:900; letter-spacing:1.5px; text-transform:uppercase; color:#ffffff; line-height:1.2;">
        {clean_title}
      </td>
      <td align="right" style="font-family:'Courier New',monospace; font-size:10px; font-weight:800; letter-spacing:1px; text-transform:uppercase; color:#ffffff; white-space:nowrap; padding-left:8px;">
        <span style="background:#b8332a; color:#ffffff; padding:3px 8px; border:1px solid rgba(255,255,255,0.4); display:inline-block; line-height:1;">{badge}</span>
      </td>
    </tr>
  </table>
</div>'''

    s = re.sub(r'<h2[^>]*>(.*?)</h2>', replace_h2, s, flags=re.IGNORECASE | re.DOTALL)

    # Transform light/faint divider headers into dark solid letterpress ribbons
    s = re.sub(
        r'<div style="border-top:2px solid #111111;\s*border-bottom:1px solid #111111;\s*padding:6px 0;\s*margin:[^"]*">',
        '<div style="background:#0a0a0a; border:1px solid #000000; padding:10px 14px; margin:34px 0 16px 0;">',
        s,
        flags=re.IGNORECASE
    )
    s = re.sub(
        r'<div style="background:#181818;\s*border:1px solid #000000;\s*padding:[^"]*;\s*margin:[^"]*">',
        '<div style="background:#0a0a0a; border:1px solid #000000; padding:10px 14px; margin:34px 0 16px 0;">',
        s,
        flags=re.IGNORECASE
    )

    # Ensure header title typography inside tables is ultra-dark, bold and legible white
    s = re.sub(
        r'<td align="left" style="font-family:[^;]+;\s*font-size:[^;]+;\s*font-weight:[^;]+;\s*letter-spacing:[^;]+;\s*text-transform:uppercase;\s*color:#111111;">',
        '<td align="left" style="font-family:\'Playfair Display\',Georgia,\'Times New Roman\',serif; font-size:14px; font-weight:900; letter-spacing:1.5px; text-transform:uppercase; color:#ffffff; line-height:1.2;">',
        s,
        flags=re.IGNORECASE
    )
    s = re.sub(
        r'<td align="left" style="font-family:\'Playfair Display\',Georgia,serif;\s*font-size:13\.5px;\s*font-weight:900;\s*letter-spacing:1\.5px;\s*text-transform:uppercase;\s*color:#ffffff;">',
        '<td align="left" style="font-family:\'Playfair Display\',Georgia,\'Times New Roman\',serif; font-size:14px; font-weight:900; letter-spacing:1.5px; text-transform:uppercase; color:#ffffff; line-height:1.2;">',
        s,
        flags=re.IGNORECASE
    )

    # 2. Convert modern rounded buttons (purple, blue, green, etc.) to vintage letterpress buttons
    s = re.sub(
        r'<a([^>]+)style="([^"]*?)background:\s*#(?:4f46e5|4338ca|6366f1|2563eb|1d4ed8|3b82f6|059669|e11d48)([^"]*?)"([^>]*)>(.*?)</a>',
        r'<a\1style="background:#ede8dc; color:#111111; border:1px solid #1a1a1a; padding:5px 12px; font-family:\'Courier New\',monospace; font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:1px; text-decoration:none; display:inline-block;"\4>\5</a>',
        s,
        flags=re.IGNORECASE | re.DOTALL
    )

    # 3. Modern neon colors -> Authentic vintage newspaper ink & letterpress palette
    color_replacements = [
        (r'#059669', '#b8332a'),  # Neon green -> letterpress red
        (r'#e11d48', '#b8332a'),  # Neon pink -> letterpress red
        (r'#0284c7', '#111111'),  # Cyan -> dense ink black
        (r'#65a30d', '#111111'),  # Lime -> dense ink black
        (r'#dc2626', '#b8332a'),  # Bright red -> letterpress red
        (r'#2563eb', '#111111'),  # Neon blue -> dense ink black
        (r'#4f46e5', '#111111'),  # Modern purple -> dense ink black
        (r'#7c3aed', '#111111'),  # Violet -> dense ink black
        (r'#1e3a8a', '#111111'),  # Blue title -> black
        (r'#3b82f6', '#444444'),  # Blue subtitle -> editorial charcoal
        (r'#c2410c', '#b8332a'),  # Orange -> letterpress red
        (r'#f97316', '#b8332a'),  # Orange gradient -> letterpress red
        (r'#ef4444', '#b8332a'),  # Bright red -> letterpress red
    ]
    for pattern, replacement in color_replacements:
        s = re.sub(pattern, replacement, s, flags=re.IGNORECASE)

    # 4. Pastel card backgrounds & modern borders -> aged newsprint tones & dark rules
    pastel_replacements = [
        (r'#ecfdf5', '#fbf9f4'),
        (r'#fff1f2', '#fbf9f4'),
        (r'#f0f9ff', '#fbf9f4'),
        (r'#f7fee7', '#fbf9f4'),
        (r'#fef2f2', '#fbf9f4'),
        (r'#eff6ff', '#fbf9f4'),
        (r'#eef2ff', '#fbf9f4'),
        (r'#fff7ed', '#ede9df'),
        (r'#f3e8ff', '#fbf9f4'),
        (r'#fdfeff', '#fcfbf8'),
        (r'#f8fafc', '#fbf9f4'),
        (r'#fce7f3', '#1a1a1a'),
        (r'#e0f2fe', '#1a1a1a'),
        (r'#ecfccb', '#1a1a1a'),
        (r'#fee2e2', '#1a1a1a'),
        (r'#dbeafe', '#1a1a1a'),
        (r'#e2e8f0', '#d4cebf'),
        (r'#f3f4f6', '#d4cebf'),
    ]
    for pattern, replacement in pastel_replacements:
        s = re.sub(pattern, replacement, s, flags=re.IGNORECASE)

    # 5. Strip modern bubble radii and drop shadows
    s = re.sub(r'border-radius:\s*(?:6|8|10|12|14|16|20|30)px;', 'border-radius:0px;', s, flags=re.IGNORECASE)
    s = re.sub(r'box-shadow:[^;]+;', '', s, flags=re.IGNORECASE)

    # 6. Mobile word-break & padding optimization
    s = s.replace('text-decoration:none;', 'text-decoration:none; word-break:break-word; overflow-wrap:break-word;')
    s = s.replace('padding:24px;', 'padding:16px 14px;')
    s = s.replace('padding:20px;', 'padding:14px 14px;')
    s = s.replace('line-height:1.75;', 'line-height:1.6; word-break:break-word; overflow-wrap:break-word;')
    s = s.replace('line-height:1.7;', 'line-height:1.55; word-break:break-word; overflow-wrap:break-word;')

    return s


def build_vintage_email_html(
    body_html: str,
    citations: List[Dict[str, str]] | None = None,
    today: str = "Wednesday, November 18, 2026",
    short_date: str = "Nov 18, 2026",
    edition: int = 1,
) -> str:
    """
    Wraps the 9-section body into the authentic vintage newspaper broadsheet email.
    Fully responsive for mobile phones (iOS, Android, Gmail App, Outlook) and desktop.
    """
    citations = citations or []
    edition_str = f"{edition:03d}"
    month_label = short_date.split()[0].upper() if short_date else "NOV"
    
    # Apply complete vintage aesthetic harmonization and mobile-first optimization
    vintage_body = sanitize_to_vintage_theme(body_html)

    # Assemble Sources Bibliography with vintage newsprint styling
    citations_html = ""
    if citations:
        source_items = ""
        for idx, chunk in enumerate(citations, 1):
            title = escape(chunk.get("title", "Article Reference"))
            url = chunk.get("url", "#")
            bg = "#ffffff" if idx % 2 == 0 else "#f8f6f0"
            source_items += f"""
            <tr>
              <td style="padding:8px 12px; font-size:11.5px; color:#222222; background:{bg}; border-bottom:1px solid #d4cebf; line-height:1.45; font-family:Georgia,serif; word-break:break-word; overflow-wrap:anywhere;">
                <span style="color:#b8332a; font-family:'Courier New',monospace; font-weight:700; margin-right:4px;">[{idx:02d}]</span>
                <a href="{url}" target="_blank" style="color:#111111; text-decoration:underline;">{title}</a>
              </td>
            </tr>"""
        citations_html = f"""
        <div style="margin-top:28px; margin-bottom:20px;">
          <div style="font-family:'Courier New',monospace; font-size:10px; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; color:#111111; border-bottom:1px solid #1a1a1a; padding-bottom:4px; margin-bottom:8px;">
            OFFICIAL GROUNDED SOURCES &amp; CITATIONS
          </div>
          <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border:1px solid #1a1a1a; table-layout:fixed; width:100%;">
            {source_items}
          </table>
        </div>"""

    return f"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0" />
  <meta name="x-apple-disable-message-reformatting" />
  <meta name="color-scheme" content="light" />
  <meta name="supported-color-schemes" content="light" />
  <title>TechAi Samachar — {short_date} — Issue #{edition_str}</title>
  <style type="text/css">
    /* ─── FLUID RESPONSIVE STYLES FOR MOBILE PHONES ─── */
    @media only screen and (max-width: 600px) {{
      .mobile-outer-pad {{
        padding: 6px 3px !important;
      }}
      .mobile-sheet-pad {{
        padding-left: 10px !important;
        padding-right: 10px !important;
      }}
      .mobile-masthead-title {{
        font-size: 34px !important;
        letter-spacing: 1px !important;
        line-height: 1 !important;
      }}
      .mobile-brand-subtitle {{
        font-size: 10px !important;
        letter-spacing: 2px !important;
      }}
      .mobile-tagline {{
        font-size: 11px !important;
        line-height: 1.4 !important;
      }}
      .mobile-meta-cell {{
        display: table-cell !important;
        font-size: 9px !important;
      }}
    }}
  </style>
</head>
<body style="margin:0; padding:0; background-color:#eae6dc; font-family:Georgia,'Times New Roman',serif; -webkit-text-size-adjust:100%; -ms-text-size-adjust:100%; word-break:break-word; overflow-wrap:break-word;">

<!-- Outer Desk Canvas -->
<table border="0" cellpadding="0" cellspacing="0" width="100%" class="mobile-outer-pad" style="background-color:#eae6dc; padding:18px 6px;">
<tr>
  <td align="center">

    <!-- Vintage Broadside Container (Fluid max 640px) -->
    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:640px; background:#fcfbf8; border:1px solid #1a1a1a; box-shadow:0 6px 24px rgba(0,0,0,0.12); table-layout:fixed;">

      <!-- TOP RULE: Hairline -->
      <tr>
        <td class="mobile-sheet-pad" style="padding:12px 18px 6px 18px;">
          <div style="border-top:1px solid #1a1a1a; height:1px; line-height:1px;"></div>
        </td>
      </tr>

      <!-- VINTAGE MASTHEAD: Fluid responsive header matching reference image -->
      <tr>
        <td class="mobile-sheet-pad" style="padding:0 18px 8px 18px;">
          <table border="0" cellpadding="0" cellspacing="0" width="100%">
            <!-- Top meta row for issue and stamp -->
            <tr>
              <td align="left" valign="middle" class="mobile-meta-cell" style="padding-bottom:4px; font-family:'Courier New',Courier,monospace; font-size:10px; font-weight:700; color:#111111; letter-spacing:1px;">
                N&deg; / {month_label}
                <span style="display:inline-block; background:#b8332a; color:#ffffff; font-family:'Courier New',monospace; font-size:8.5px; font-weight:bold; padding:2px 6px; border:1px solid #1a1a1a; text-transform:uppercase; margin-left:6px; vertical-align:middle;">
                  PRESS
                </span>
              </td>
              <td align="right" valign="middle" class="mobile-meta-cell" style="padding-bottom:4px; font-family:'Courier New',Courier,monospace; font-size:10px; font-weight:700; color:#555555;">
                <span style="color:#b8332a; font-family:'Playfair Display',Georgia,serif; font-size:15px; font-weight:900;"># {edition_str}</span> &bull; 8:30 AM IST
              </td>
            </tr>
          </table>

          <!-- Central Title Block: Centered & Fluid for Phones -->
          <div style="text-align:center; padding:6px 0 2px 0;">
            <div class="mobile-brand-subtitle" style="font-family:'Courier New',Courier,monospace; font-size:11px; font-weight:700; color:#111111; letter-spacing:3px; text-transform:uppercase; margin-bottom:2px;">
              T E C H A I &nbsp; S A M A C H A R
            </div>
            <h1 class="mobile-masthead-title" style="margin:0; font-family:'Playfair Display',Georgia,'Times New Roman',serif; font-size:44px; font-weight:900; color:#111111; letter-spacing:2px; line-height:0.95; text-transform:uppercase;">
              N E W S
            </h1>
            <div class="mobile-tagline" style="font-family:Georgia,'Times New Roman',serif; font-size:12px; font-style:italic; color:#444444; letter-spacing:0.3px; margin-top:4px; line-height:1.4;">
              Daily Briefing &amp; Analysis &bull; The Daily AI &amp; Silicon Chronicle
            </div>
          </div>
        </td>
      </tr>

      <!-- DOUBLE RULE DIVIDER -->
      <tr>
        <td class="mobile-sheet-pad" style="padding:0 18px;">
          <div style="border-top:1px solid #1a1a1a; border-bottom:2px solid #1a1a1a; height:3px; line-height:3px;"></div>
        </td>
      </tr>

      <!-- DATE & METADATA BAR -->
      <tr>
        <td class="mobile-sheet-pad" style="padding:4px 18px;">
          <table border="0" cellpadding="0" cellspacing="0" width="100%">
            <tr>
              <td align="left" style="font-family:'Courier New',monospace; font-size:9px; font-weight:700; color:#555555; letter-spacing:1px; text-transform:uppercase;">
                DAILY INTELLIGENCE &bull; INDIA &amp; GLOBAL
              </td>
              <td align="right" style="font-family:'Courier New',monospace; font-size:9px; font-weight:700; color:#111111; letter-spacing:0.5px; text-transform:uppercase;">
                {today}
              </td>
            </tr>
          </table>
        </td>
      </tr>

      <!-- SECONDARY RULE -->
      <tr>
        <td class="mobile-sheet-pad" style="padding:0 18px 12px 18px;">
          <div style="border-top:1px solid #1a1a1a; height:1px; line-height:1px;"></div>
        </td>
      </tr>

      <!-- INTRO GREETING CARD (Vintage dispatch panel) -->
      <tr>
        <td class="mobile-sheet-pad" style="padding:0 18px 18px 18px;">
          <div style="background:#ede9df; border:1px solid #1a1a1a; padding:10px 14px;">
            <p style="margin:0; font-family:Georgia,serif; font-style:italic; font-size:12.5px; color:#222222; line-height:1.55;">
              Good morning! &#9728;&#65039; Here is your complete morning tech briefing: AI breakthroughs, phone &amp; laptop launches, Nvidia &amp; GPU silicon, China tech moves, Big Tech developments, and upcoming events. Curated and verified for today.
            </p>
          </div>
        </td>
      </tr>

      <!-- 9 COMPREHENSIVE SECTIONS BODY (Harmonized Vintage Newspaper Style) -->
      <tr>
        <td class="mobile-sheet-pad" style="padding:0 18px;">
          {vintage_body}
        </td>
      </tr>

      <!-- CITATIONS & REFERENCES -->
      <tr>
        <td class="mobile-sheet-pad" style="padding:0 18px;">
          {citations_html}
        </td>
      </tr>

      <!-- VINTAGE FOOTER & COLOPHON -->
      <tr>
        <td class="mobile-sheet-pad" style="border-top:2px solid #1a1a1a; padding:20px 18px; text-align:center; background:#ede9df;">
          <div style="font-family:'Playfair Display',Georgia,serif; font-size:18px; font-weight:900; color:#111111; text-transform:uppercase; letter-spacing:1px; margin-bottom:4px;">
            TECHAI SAMACHAR PRESS
          </div>
          <p style="margin:0 0 4px 0; font-family:'Courier New',monospace; font-size:10.5px; color:#444444; font-weight:600; letter-spacing:1px; text-transform:uppercase;">
            Curated by {EDITOR_NAME} &bull; {EDITOR_TITLE}
          </p>
          <div style="font-family:Georgia,serif; font-size:13px; color:#111111; margin:8px 0;">
            &#10086; &nbsp; &bull; &nbsp; &#10087; &nbsp; &bull; &nbsp; &#10086;
          </div>

          <table border="0" cellpadding="0" cellspacing="0" style="margin:0 auto 10px auto;">
            <tr>
              <td style="padding:0 6px;">
                <a href="#" style="font-family:'Courier New',monospace; font-size:9.5px; font-weight:700; color:#111111; text-decoration:none; text-transform:uppercase;">Unsubscribe</a>
              </td>
              <td style="color:#777777; font-size:9.5px;">|</td>
              <td style="padding:0 6px;">
                <a href="#" style="font-family:'Courier New',monospace; font-size:9.5px; font-weight:700; color:#111111; text-decoration:none; text-transform:uppercase;">Archives</a>
              </td>
              <td style="color:#777777; font-size:9.5px;">|</td>
              <td style="padding:0 6px;">
                <a href="#" style="font-family:'Courier New',monospace; font-size:9.5px; font-weight:700; color:#111111; text-decoration:none; text-transform:uppercase;">Feedback</a>
              </td>
            </tr>
          </table>

          <p style="margin:0; font-family:Georgia,serif; font-size:10px; font-style:italic; color:#666666; line-height:1.5;">
            Delivered every morning at 8:30 AM IST &bull; Powered by Gemini AI + Google Search Grounding<br/>
            &copy; 2026 TechAi Samachar. All rights reserved.
          </p>
        </td>
      </tr>

    </table>

  </td>
</tr>
</table>

</body>
</html>"""


def build_vintage_web_html(
    email_html: str,
    short_date: str = "Nov 18, 2026",
    edition: int = 1,
) -> str:
    """
    Builds the rich 'vintage online' webpage with authentic newspaper styling,
    custom fonts, grain texture, reader mode controls, and responsive layout.
    """
    edition_str = f"{edition:03d}"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TechAi Samachar — Vintage Online Edition #{edition_str}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&family=EB+Garamond:ital,wght@0,400;0,600;0,800;1,400;1,600&family=Playfair+Display:ital,wght@0,700;0,900;1,400;1,700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-desk: #2b2723;
      --bg-paper: #f6f4ee;
      --ink: #111111;
      --accent-red: #b8332a;
    }}
    
    body.sepia-theme {{
      --bg-desk: #1f1814;
      --bg-paper: #f0e8d4;
      --ink: #221a14;
    }}

    * {{ box-sizing: border-box; }}
    
    body {{
      margin: 0;
      padding: 0;
      background-color: var(--bg-desk);
      background-image: radial-gradient(rgba(255,255,255,0.04) 1px, transparent 1px);
      background-size: 24px 24px;
      color: var(--ink);
      font-family: 'EB Garamond', Georgia, serif;
      -webkit-font-smoothing: antialiased;
    }}

    /* Top Floating Vintage Control Toolbar */
    .top-toolbar {{
      position: sticky;
      top: 0;
      z-index: 1000;
      background: rgba(22, 18, 15, 0.96);
      backdrop-filter: blur(8px);
      border-bottom: 1px solid #443a32;
      padding: 10px 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 4px 20px rgba(0,0,0,0.4);
      flex-wrap: wrap;
      gap: 8px;
    }}
    .toolbar-brand {{
      color: #f6f4ee;
      font-family: 'Cinzel', serif;
      font-size: 13px;
      letter-spacing: 1.5px;
      font-weight: 700;
    }}
    .toolbar-actions {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }}
    .vintage-btn {{
      background: #332822;
      border: 1px solid #5a493e;
      color: #f6f4ee;
      padding: 6px 12px;
      font-family: 'Space Mono', monospace;
      font-size: 10.5px;
      font-weight: 700;
      text-transform: uppercase;
      cursor: pointer;
      border-radius: 3px;
      transition: all 0.2s ease;
    }}
    .vintage-btn:hover {{
      background: var(--accent-red);
      border-color: var(--accent-red);
      color: #ffffff;
    }}

    /* Main Newspaper Canvas */
    .newspaper-wrap {{
      max-width: 680px;
      margin: 24px auto;
      padding: 0 8px;
    }}

    .newspaper-sheet {{
      background-color: var(--bg-paper);
      box-shadow: 0 16px 50px rgba(0,0,0,0.5), 0 0 0 1px rgba(0,0,0,0.2);
      position: relative;
      overflow: hidden;
    }}

    /* Paper grain overlay */
    .newspaper-sheet::before {{
      content: "";
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      pointer-events: none;
      opacity: 0.035;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
    }}

    /* Print View Styles */
    @media print {{
      body {{ background: #ffffff; }}
      .top-toolbar {{ display: none; }}
      .newspaper-wrap {{ max-width: 100%; margin: 0; padding: 0; }}
      .newspaper-sheet {{ box-shadow: none; border: none; }}
    }}
  </style>
</head>
<body>

  <!-- Top Vintage Online Toolbar -->
  <div class="top-toolbar">
    <div class="toolbar-brand">
      &#128240; TECHAI SAMACHAR &bull; VINTAGE ONLINE
    </div>
    <div class="toolbar-actions">
      <button class="vintage-btn" onclick="document.body.classList.toggle('sepia-theme')">&#127912; Paper Tint</button>
      <button class="vintage-btn" onclick="window.print()">&#128424; Print PDF</button>
      <button class="vintage-btn" onclick="copyEmailHtml()">&#128203; Copy HTML</button>
    </div>
  </div>

  <!-- Newspaper Viewer -->
  <div class="newspaper-wrap">
    <div class="newspaper-sheet">
      {email_html}
    </div>
  </div>

  <textarea id="rawEmailHtml" style="display:none;">{escape(email_html)}</textarea>

  <script>
    function copyEmailHtml() {{
      const text = document.getElementById('rawEmailHtml').value;
      navigator.clipboard.writeText(text).then(() => {{
        alert('Email HTML copied to clipboard! You can paste directly into an email sender or campaign template.');
      }});
    }}
  </script>
</body>
</html>"""
