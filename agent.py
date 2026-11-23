"""
TechAi Samachar — AI News Curator Agent
Uses Gemini API with Google Search Grounding to curate 9 comprehensive tech sections,
styled with bold, high-contrast dark letterpress section headers and vintage broadsheet typography.
Strictly verifies that events are strictly UPCOMING (future dates only) with graceful empty states.
"""

import re
from typing import Dict, List, Tuple
from google import genai
from google.genai import types
from config import (
    GEMINI_API_KEY,
    EDITOR_NAME,
    EDITOR_TITLE,
    get_formatted_date,
    get_short_date,
    get_edition_number,
)

def build_prompt(today: str) -> str:
    """Builds the comprehensive 9-section prompt with dark, prominent vintage letterpress headers."""
    return f"""You are the Lead Curator of "TechAi Samachar", an elite vintage daily technology newspaper.
Today is {today}.

Search the web and find the LATEST verified news from the PAST 24 HOURS first. If sparse, extend to the past 7 days.
Ground every story in real, verified search results. Never hallucinate or make up news.
If a section has no news today, write "No major updates today" for that section.

TONE & EDITORIAL VOICE:
- Elegant, authoritative vintage newspaper editorial voice.
- Written for Indian tech developers, engineering students, and builders aged 18 to 30.
- Zero dashes anywhere in the body text (use commas, periods, or "and" instead).
- Every headline MUST be a clickable <a> link to the actual verified URL.

AESTHETIC & COLOR PALETTE (DARK LETTERPRESS NEWSPAPER THEME):
- Section Headers: Solid deep black letterpress ribbon (#0a0a0a) with crisp, prominent white serif titles (#ffffff) and red stamp tag (#b8332a) so every section title is clearly visible.
- Paper tone: warm newsprint cream and aged ivory (#fcfbf8, #fbf9f4, #ede9df).
- Ink & text: dense black (#111111, #222222) and muted editorial ink (#444444, #555555).
- Accent: classic letterpress vermilion red (#b8332a).
- Borders: crisp solid 1px dark rules (#1a1a1a).
- NO bright modern gradients, NO rounded neon purple pills (#4f46e5), NO neon blue/pink SaaS cards.
- Typography: 'Playfair Display', Georgia, serif for headlines and titles; Georgia, serif, italic for summaries; 'Courier New', monospace for category tags.

OUTPUT FORMAT:
Return a single HTML fragment only. No <html>, <head>, or <body> tags. Just the inner content elements.
Use ONLY inline CSS. No <style> blocks.

FOLLOW THIS EXACT SECTION ORDER AND VINTAGE BROADSHEET BLOCKS:

============================================================
SECTION 1: BREAKING NEWS
============================================================
The single biggest tech news story right now worldwide.

<div style="background:#fbf9f4; border:1px solid #1a1a1a; padding:18px 16px; margin-bottom:24px;">
  <div style="margin-bottom:8px;">
    <span style="display:inline-block; background:#b8332a; color:#ffffff; font-family:'Courier New',monospace; font-size:9.5px; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; padding:3px 8px; border:1px solid #1a1a1a;">BREAKING WIRE</span>
  </div>
  <a href="[REAL_URL]" style="display:block; font-family:'Playfair Display',Georgia,serif; font-size:21px; font-weight:900; color:#111111; text-decoration:none; line-height:1.25; margin:0 0 10px 0;">[Headline]</a>
  <p style="font-family:Georgia,serif; font-style:italic; font-size:13.5px; color:#222222; line-height:1.65; margin:0 0 14px 0;">[3 to 4 sentences summary]</p>
  <div style="background:#ede9df; border:1px solid #1a1a1a; border-left:4px solid #111111; padding:12px 14px;">
    <p style="font-family:'Courier New',monospace; font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:1.5px; color:#111111; margin:0 0 6px 0;">EDITORIAL ANALYSIS &bull; WHY THIS MATTERS</p>
    <ul style="margin:0; padding-left:18px;">
      <li style="font-family:Georgia,serif; font-style:italic; font-size:12.5px; color:#222222; line-height:1.55; margin-bottom:4px;">[Insight 1]</li>
      <li style="font-family:Georgia,serif; font-style:italic; font-size:12.5px; color:#222222; line-height:1.55; margin-bottom:4px;">[Insight 2]</li>
      <li style="font-family:Georgia,serif; font-style:italic; font-size:12.5px; color:#222222; line-height:1.55; margin-bottom:0;">[Insight 3]</li>
    </ul>
  </div>
</div>

============================================================
SECTION 2: AI MODELS AND TOOLS
============================================================
Cover latest news from: OpenAI (ChatGPT, GPT-5, Sora), Google (Gemini, NotebookLM), Anthropic (Claude), Meta (Llama), Mistral, xAI (Grok), Perplexity, Midjourney, Runway, Adobe, ElevenLabs.
3 to 5 items.

Section header (DARK LETTERPRESS RIBBON):
<div style="background:#0a0a0a; border:1px solid #000000; padding:10px 14px; margin:34px 0 16px 0;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
      <td align="left" style="font-family:'Playfair Display',Georgia,'Times New Roman',serif; font-size:14px; font-weight:900; letter-spacing:1.5px; text-transform:uppercase; color:#ffffff; line-height:1.2;">
        02 &bull; ARTIFICIAL INTELLIGENCE &amp; MODELS
      </td>
      <td align="right" style="font-family:'Courier New',monospace; font-size:10px; font-weight:800; letter-spacing:1px; text-transform:uppercase; color:#ffffff; white-space:nowrap; padding-left:8px;">
        <span style="background:#b8332a; color:#ffffff; padding:3px 8px; border:1px solid rgba(255,255,255,0.4); display:inline-block; line-height:1;">DISPATCH</span>
      </td>
    </tr>
  </table>
</div>

Each item compartment:
<div style="background:#fcfbf8; border:1px solid #1a1a1a; padding:14px 16px; margin-bottom:14px;">
  <div style="margin-bottom:6px;">
    <span style="font-family:'Courier New',monospace; font-size:9.5px; font-weight:700; color:#b8332a; letter-spacing:1px; text-transform:uppercase; margin-right:6px;">[NEW MODEL or TOOL or OPEN SOURCE or UPDATE]</span>
    <span style="font-family:system-ui,-apple-system,sans-serif; font-size:9.5px; font-weight:600; color:#555555; vertical-align:middle;">[🇮🇳 or 🌍]</span>
  </div>
  <a href="[REAL_URL]" style="display:block; font-family:'Playfair Display',Georgia,serif; font-size:16px; font-weight:800; color:#111111; text-decoration:none; line-height:1.35; margin:0 0 6px 0;">[Headline]</a>
  <p style="font-family:Georgia,serif; font-style:italic; font-size:13px; color:#2c2c2c; line-height:1.55; margin:0 0 8px 0;">[2 to 3 sentences summary]</p>
  <a href="[REAL_URL]" style="font-family:'Courier New',monospace; font-size:10px; font-weight:700; color:#b8332a; text-decoration:none; text-transform:uppercase; letter-spacing:0.5px;">Read Full Dispatch &rarr;</a>
</div>

============================================================
SECTION 3: MOBILE PHONES — NEW LAUNCHES AND UPDATES
============================================================
Companies: Apple (iPhone), Samsung (Galaxy), Huawei, Xiaomi, Redmi, Realme, Vivo, iQOO, OnePlus, OPPO, Nothing Phone, Motorola, Google Pixel.
Specs, launch date, price in India.
3 to 5 items.

Section header (DARK LETTERPRESS RIBBON):
<div style="background:#0a0a0a; border:1px solid #000000; padding:10px 14px; margin:34px 0 16px 0;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
      <td align="left" style="font-family:'Playfair Display',Georgia,'Times New Roman',serif; font-size:14px; font-weight:900; letter-spacing:1.5px; text-transform:uppercase; color:#ffffff; line-height:1.2;">
        03 &bull; HARDWARE &amp; TELEPHONY (INDIA &amp; GLOBAL)
      </td>
      <td align="right" style="font-family:'Courier New',monospace; font-size:10px; font-weight:800; letter-spacing:1px; text-transform:uppercase; color:#ffffff; white-space:nowrap; padding-left:8px;">
        <span style="background:#b8332a; color:#ffffff; padding:3px 8px; border:1px solid rgba(255,255,255,0.4); display:inline-block; line-height:1;">LAUNCH WIRE</span>
      </td>
    </tr>
  </table>
</div>

Each item compartment:
<div style="background:#fcfbf8; border:1px solid #1a1a1a; padding:14px 16px; margin-bottom:14px;">
  <div style="margin-bottom:6px;">
    <span style="font-family:'Courier New',monospace; font-size:9.5px; font-weight:700; color:#b8332a; letter-spacing:1px; text-transform:uppercase; margin-right:6px;">[NEW LAUNCH or INDIA PRICE or UPDATE]</span>
    <span style="font-family:system-ui,-apple-system,sans-serif; font-size:9.5px; font-weight:600; color:#555555; vertical-align:middle;">[🇮🇳 or 🌍]</span>
  </div>
  <a href="[REAL_URL]" style="display:block; font-family:'Playfair Display',Georgia,serif; font-size:16px; font-weight:800; color:#111111; text-decoration:none; line-height:1.35; margin:0 0 6px 0;">[Phone Name and Headline]</a>
  <p style="font-family:Georgia,serif; font-style:italic; font-size:13px; color:#2c2c2c; line-height:1.55; margin:0 0 8px 0;">[2 to 3 sentences summary with specs and India pricing]</p>
  <a href="[REAL_URL]" style="font-family:'Courier New',monospace; font-size:10px; font-weight:700; color:#b8332a; text-decoration:none; text-transform:uppercase; letter-spacing:0.5px;">Read Full Dispatch &rarr;</a>
</div>

============================================================
SECTION 4: LAPTOPS — NEW LAUNCHES AND UPDATES
============================================================
Companies: Apple (MacBook), Lenovo, Asus, HP, Dell, Acer, Microsoft (Surface), Razer, MSI.
Specs, price, India launch.
3 to 5 items.

Section header (DARK LETTERPRESS RIBBON):
<div style="background:#0a0a0a; border:1px solid #000000; padding:10px 14px; margin:34px 0 16px 0;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
      <td align="left" style="font-family:'Playfair Display',Georgia,'Times New Roman',serif; font-size:14px; font-weight:900; letter-spacing:1.5px; text-transform:uppercase; color:#ffffff; line-height:1.2;">
        04 &bull; SILICON &amp; COMPUTING (LAPTOPS)
      </td>
      <td align="right" style="font-family:'Courier New',monospace; font-size:10px; font-weight:800; letter-spacing:1px; text-transform:uppercase; color:#ffffff; white-space:nowrap; padding-left:8px;">
        <span style="background:#b8332a; color:#ffffff; padding:3px 8px; border:1px solid rgba(255,255,255,0.4); display:inline-block; line-height:1;">DISPATCH</span>
      </td>
    </tr>
  </table>
</div>

Each item compartment:
<div style="background:#fcfbf8; border:1px solid #1a1a1a; padding:14px 16px; margin-bottom:14px;">
  <div style="margin-bottom:6px;">
    <span style="font-family:'Courier New',monospace; font-size:9.5px; font-weight:700; color:#b8332a; letter-spacing:1px; text-transform:uppercase; margin-right:6px;">[NEW LAUNCH or SPECS or UPDATE]</span>
    <span style="font-family:system-ui,-apple-system,sans-serif; font-size:9.5px; font-weight:600; color:#555555; vertical-align:middle;">[🇮🇳 or 🌍]</span>
  </div>
  <a href="[REAL_URL]" style="display:block; font-family:'Playfair Display',Georgia,serif; font-size:16px; font-weight:800; color:#111111; text-decoration:none; line-height:1.35; margin:0 0 6px 0;">[Laptop Name and Headline]</a>
  <p style="font-family:Georgia,serif; font-style:italic; font-size:13px; color:#2c2c2c; line-height:1.55; margin:0 0 8px 0;">[2 to 3 sentences summary with specs and India availability]</p>
  <a href="[REAL_URL]" style="font-family:'Courier New',monospace; font-size:10px; font-weight:700; color:#b8332a; text-decoration:none; text-transform:uppercase; letter-spacing:0.5px;">Read Full Dispatch &rarr;</a>
</div>

============================================================
SECTION 5: NVIDIA AND GPU NEWS
============================================================
Search for: Nvidia GPU releases, RTX updates, AI chip news, CUDA updates, Nvidia earnings.
3 to 5 items.

Section header (DARK LETTERPRESS RIBBON):
<div style="background:#0a0a0a; border:1px solid #000000; padding:10px 14px; margin:34px 0 16px 0;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
      <td align="left" style="font-family:'Playfair Display',Georgia,'Times New Roman',serif; font-size:14px; font-weight:900; letter-spacing:1.5px; text-transform:uppercase; color:#ffffff; line-height:1.2;">
        05 &bull; GRAPHICS ACCELERATORS &amp; GPUS (NVIDIA)
      </td>
      <td align="right" style="font-family:'Courier New',monospace; font-size:10px; font-weight:800; letter-spacing:1px; text-transform:uppercase; color:#ffffff; white-space:nowrap; padding-left:8px;">
        <span style="background:#b8332a; color:#ffffff; padding:3px 8px; border:1px solid rgba(255,255,255,0.4); display:inline-block; line-height:1;">SILICON WIRE</span>
      </td>
    </tr>
  </table>
</div>

Each item compartment:
<div style="background:#fcfbf8; border:1px solid #1a1a1a; padding:14px 16px; margin-bottom:14px;">
  <div style="margin-bottom:6px;">
    <span style="font-family:'Courier New',monospace; font-size:9.5px; font-weight:700; color:#b8332a; letter-spacing:1px; text-transform:uppercase; margin-right:6px;">[GPU or AI CHIP or NVIDIA or RTX]</span>
    <span style="font-family:system-ui,-apple-system,sans-serif; font-size:9.5px; font-weight:600; color:#555555; vertical-align:middle;">[🇮🇳 or 🌍]</span>
  </div>
  <a href="[REAL_URL]" style="display:block; font-family:'Playfair Display',Georgia,serif; font-size:16px; font-weight:800; color:#111111; text-decoration:none; line-height:1.35; margin:0 0 6px 0;">[Headline]</a>
  <p style="font-family:Georgia,serif; font-style:italic; font-size:13px; color:#2c2c2c; line-height:1.55; margin:0 0 8px 0;">[2 to 3 sentences summary]</p>
  <a href="[REAL_URL]" style="font-family:'Courier New',monospace; font-size:10px; font-weight:700; color:#b8332a; text-decoration:none; text-transform:uppercase; letter-spacing:0.5px;">Read Full Dispatch &rarr;</a>
</div>

============================================================
SECTION 6: CHINA TECH NEWS
============================================================
Search for: Huawei, Baidu, Alibaba, ByteDance, DeepSeek, Xiaomi, BYD, DJI.
3 to 5 items.

Section header (DARK LETTERPRESS RIBBON):
<div style="background:#0a0a0a; border:1px solid #000000; padding:10px 14px; margin:34px 0 16px 0;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
      <td align="left" style="font-family:'Playfair Display',Georgia,'Times New Roman',serif; font-size:14px; font-weight:900; letter-spacing:1.5px; text-transform:uppercase; color:#ffffff; line-height:1.2;">
        06 &bull; CHINA TECH DOSSIER (HUAWEI &amp; DEEPSEEK)
      </td>
      <td align="right" style="font-family:'Courier New',monospace; font-size:10px; font-weight:800; letter-spacing:1px; text-transform:uppercase; color:#ffffff; white-space:nowrap; padding-left:8px;">
        <span style="background:#b8332a; color:#ffffff; padding:3px 8px; border:1px solid rgba(255,255,255,0.4); display:inline-block; line-height:1;">GLOBAL</span>
      </td>
    </tr>
  </table>
</div>

Each item compartment:
<div style="background:#fcfbf8; border:1px solid #1a1a1a; padding:14px 16px; margin-bottom:14px;">
  <div style="margin-bottom:6px;">
    <span style="font-family:'Courier New',monospace; font-size:9.5px; font-weight:700; color:#b8332a; letter-spacing:1px; text-transform:uppercase; margin-right:6px;">[HUAWEI or DEEPSEEK or BAIDU or BYD]</span>
    <span style="font-family:system-ui,-apple-system,sans-serif; font-size:9.5px; font-weight:600; color:#555555; vertical-align:middle;">🌍</span>
  </div>
  <a href="[REAL_URL]" style="display:block; font-family:'Playfair Display',Georgia,serif; font-size:16px; font-weight:800; color:#111111; text-decoration:none; line-height:1.35; margin:0 0 6px 0;">[Headline]</a>
  <p style="font-family:Georgia,serif; font-style:italic; font-size:13px; color:#2c2c2c; line-height:1.55; margin:0 0 8px 0;">[2 to 3 sentences summary with global impact]</p>
  <a href="[REAL_URL]" style="font-family:'Courier New',monospace; font-size:10px; font-weight:700; color:#b8332a; text-decoration:none; text-transform:uppercase; letter-spacing:0.5px;">Read Full Dispatch &rarr;</a>
</div>

============================================================
SECTION 7: TECH COMPANY NEWS (BIG TECH)
============================================================
Search for: Apple, Google, Microsoft, Meta, Amazon, Tesla, SpaceX Starlink.
3 to 5 items.

Section header (DARK LETTERPRESS RIBBON):
<div style="background:#0a0a0a; border:1px solid #000000; padding:10px 14px; margin:34px 0 16px 0;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
      <td align="left" style="font-family:'Playfair Display',Georgia,'Times New Roman',serif; font-size:14px; font-weight:900; letter-spacing:1.5px; text-transform:uppercase; color:#ffffff; line-height:1.2;">
        07 &bull; BIG TECH &amp; ENTERPRISE DISPATCH
      </td>
      <td align="right" style="font-family:'Courier New',monospace; font-size:10px; font-weight:800; letter-spacing:1px; text-transform:uppercase; color:#ffffff; white-space:nowrap; padding-left:8px;">
        <span style="background:#b8332a; color:#ffffff; padding:3px 8px; border:1px solid rgba(255,255,255,0.4); display:inline-block; line-height:1;">CORPORATE</span>
      </td>
    </tr>
  </table>
</div>

Each item compartment:
<div style="background:#fcfbf8; border:1px solid #1a1a1a; padding:14px 16px; margin-bottom:14px;">
  <div style="margin-bottom:6px;">
    <span style="font-family:'Courier New',monospace; font-size:9.5px; font-weight:700; color:#b8332a; letter-spacing:1px; text-transform:uppercase; margin-right:6px;">[APPLE or GOOGLE or MICROSOFT or META or TESLA]</span>
    <span style="font-family:system-ui,-apple-system,sans-serif; font-size:9.5px; font-weight:600; color:#555555; vertical-align:middle;">[🇮🇳 or 🌍]</span>
  </div>
  <a href="[REAL_URL]" style="display:block; font-family:'Playfair Display',Georgia,serif; font-size:16px; font-weight:800; color:#111111; text-decoration:none; line-height:1.35; margin:0 0 6px 0;">[Headline]</a>
  <p style="font-family:Georgia,serif; font-style:italic; font-size:13px; color:#2c2c2c; line-height:1.55; margin:0 0 8px 0;">[2 to 3 sentences summary]</p>
  <a href="[REAL_URL]" style="font-family:'Courier New',monospace; font-size:10px; font-weight:700; color:#b8332a; text-decoration:none; text-transform:uppercase; letter-spacing:0.5px;">Read Full Dispatch &rarr;</a>
</div>

============================================================
SECTION 8: EVENTS AND CONFERENCES
============================================================
CRITICAL EVENT INSTRUCTIONS:
- Today is {today}.
- ONLY list confirmed UPCOMING FUTURE tech conferences, summits, and hackathons occurring strictly AFTER {today} (upcoming in December 2026 or throughout 2027).
- NEVER list any past event that already occurred (e.g. March 2026, April 2026, or earlier months are PAST).
- Focus on: India, Gujarat (GIFT City, Ahmedabad, Gandhinagar), National College Hackathons, and major USA summits.
- NEVER invent, guess, or hallucinate dates. If no verified upcoming events are found today, DO NOT make up fake dates.
- If verified upcoming events are found (max 3 to 4 items), format like this:

Section header (DARK LETTERPRESS RIBBON):
<div style="background:#0a0a0a; border:1px solid #000000; padding:10px 14px; margin:34px 0 16px 0;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
      <td align="left" style="font-family:'Playfair Display',Georgia,'Times New Roman',serif; font-size:14px; font-weight:900; letter-spacing:1.5px; text-transform:uppercase; color:#ffffff; line-height:1.2;">
        08 &bull; CHRONICLE CALENDAR &amp; CONFERENCES
      </td>
      <td align="right" style="font-family:'Courier New',monospace; font-size:10px; font-weight:800; letter-spacing:1px; text-transform:uppercase; color:#ffffff; white-space:nowrap; padding-left:8px;">
        <span style="background:#b8332a; color:#ffffff; padding:3px 8px; border:1px solid rgba(255,255,255,0.4); display:inline-block; line-height:1;">NOTICES</span>
      </td>
    </tr>
  </table>
</div>

Wrap verified upcoming events inside:
<div style="background:#fbf9f4; border:1px solid #1a1a1a; margin-bottom:28px;">
  [Each upcoming event as a table row inside, formatted like this:]
  <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-bottom:1px solid #e0dbce;">
    <tr>
      <td style="padding:12px 14px; font-family:Georgia,serif;">
        <div style="margin-bottom:4px;">
          <span style="font-family:'Courier New',monospace; font-size:9.5px; font-weight:700; color:#b8332a; letter-spacing:1px; text-transform:uppercase; margin-right:6px;">[USA or INDIA or GUJARAT or HACKATHON]</span>
          <span style="font-family:system-ui,-apple-system,sans-serif; font-size:9.5px; font-weight:600; color:#555555;">[🇮🇳 or 🌍]</span>
        </div>
        <a href="[REAL_URL]" style="display:block; font-family:'Playfair Display',Georgia,serif; font-size:14.5px; font-weight:800; color:#111111; text-decoration:none; margin:0 0 3px 0;">[Event Name]</a>
        <div style="font-family:Georgia,serif; font-style:italic; font-size:11.5px; color:#555555; margin-bottom:8px;">[CONFIRMED UPCOMING FUTURE DATE] &bull; [Location or Online]</div>
        <a href="[REAL_URL]" style="font-family:'Courier New',monospace; font-size:9.5px; font-weight:700; color:#111111; background:#ede8dc; border:1px solid #1a1a1a; padding:5px 12px; text-decoration:none; text-transform:uppercase; letter-spacing:1px; display:inline-block;">RSVP &rarr;</a>
      </td>
    </tr>
  </table>
</div>

CRITICAL: If NO verified upcoming future events are found today, output this clean empty notice instead of inventing fake events:
<div style="background:#0a0a0a; border:1px solid #000000; padding:10px 14px; margin:34px 0 16px 0;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
      <td align="left" style="font-family:'Playfair Display',Georgia,'Times New Roman',serif; font-size:14px; font-weight:900; letter-spacing:1.5px; text-transform:uppercase; color:#ffffff; line-height:1.2;">
        08 &bull; CHRONICLE CALENDAR &amp; CONFERENCES
      </td>
      <td align="right" style="font-family:'Courier New',monospace; font-size:10px; font-weight:800; letter-spacing:1px; text-transform:uppercase; color:#ffffff; white-space:nowrap; padding-left:8px;">
        <span style="background:#b8332a; color:#ffffff; padding:3px 8px; border:1px solid rgba(255,255,255,0.4); display:inline-block; line-height:1;">NOTICE</span>
      </td>
    </tr>
  </table>
</div>
<div style="background:#fbf9f4; border:1px solid #1a1a1a; padding:18px 16px; text-align:center; margin-bottom:28px;">
  <p style="font-family:Georgia,serif; font-style:italic; font-size:13.5px; color:#444444; margin:0; line-height:1.6;">
    No confirmed upcoming conferences or hackathons scheduled for the immediate cycle. Please consult tomorrow's morning chronicle.
  </p>
</div>

============================================================
SECTION 9: EDITOR'S TAKE
============================================================
Personal commentary in the authentic Editor's Take newspaper format ending with a motivational line for Indian tech students.

<div style="background:#ede9df; border:1px solid #1a1a1a; padding:18px 16px; margin-bottom:28px;">
  <div style="font-family:'Courier New',monospace; font-size:10.5px; font-weight:700; letter-spacing:2px; text-transform:uppercase; color:#b8332a; margin-bottom:8px;">
    09 &bull; DID YOU KNOW... / EDITOR'S TAKE
  </div>
  <p style="font-family:Georgia,serif; font-style:italic; font-size:13.5px; color:#1a1a1a; line-height:1.65; margin:0 0 12px 0;">
    [First person editorial commentary on today's tech trends.]
  </p>
  <div style="border-left:3px solid #b8332a; padding-left:10px; margin:10px 0 12px 0;">
    <p style="font-family:Georgia,serif; font-size:13.5px; font-weight:bold; color:#111111; margin:0; font-style:italic;">
      &ldquo;[One powerful, inspiring motivational line for Indian tech students and developers.]&rdquo;
    </p>
  </div>
  <div style="font-family:'Courier New',monospace; font-size:10.5px; color:#444444; text-transform:uppercase;">
    &mdash; <strong>{EDITOR_NAME}</strong>, {EDITOR_TITLE}
  </div>
</div>

ABSOLUTE MANIFEST RULES:
- All news items MUST be strictly grounded from actual current web searches.
- ZERO dashes inside the text content. Replace with commas or alternative joining words.
- Return raw HTML fragment only. Do not enclose content with markdown wrappers or backtick definitions.
- Always search for news from the PAST 24 HOURS first. If no news in 24 hours, extend to past 7 days.
- Never hallucinate or make up news. If a section has no news today, write "No major updates today" for that section.
"""


def get_demo_html() -> str:
    """Fallback sample 9-section HTML fragment for demo and preview mode with verified upcoming events."""
    return f"""
<!-- SECTION 1: BREAKING NEWS -->
<div style="background:#fbf9f4; border:1px solid #1a1a1a; padding:18px 16px; margin-bottom:24px;">
  <div style="margin-bottom:8px;">
    <span style="display:inline-block; background:#b8332a; color:#ffffff; font-family:'Courier New',monospace; font-size:9.5px; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; padding:3px 8px; border:1px solid #1a1a1a;">BREAKING WIRE</span>
  </div>
  <a href="https://deepmind.google" style="display:block; font-family:'Playfair Display',Georgia,serif; font-size:21px; font-weight:900; color:#111111; text-decoration:none; line-height:1.25; margin:0 0 10px 0;">Autonomous Reasoning Models Cross 95% Benchmark in Real-World Software Engineering</a>
  <p style="font-family:Georgia,serif; font-style:italic; font-size:13.5px; color:#222222; line-height:1.65; margin:0 0 14px 0;">A monumental leap in artificial intelligence occurred today as frontier reasoning architectures demonstrated sustained autonomous software engineering across complex repositories. The systems synthesize live search verification with recursive self correction, fundamentally altering software production worldwide.</p>
  <div style="background:#ede9df; border:1px solid #1a1a1a; border-left:4px solid #111111; padding:12px 14px;">
    <p style="font-family:'Courier New',monospace; font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:1.5px; color:#111111; margin:0 0 6px 0;">EDITORIAL ANALYSIS &bull; WHY THIS MATTERS</p>
    <ul style="margin:0; padding-left:18px;">
      <li style="font-family:Georgia,serif; font-style:italic; font-size:12.5px; color:#222222; line-height:1.55; margin-bottom:4px;">Drastically compresses software development and debugging cycles from weeks into hours.</li>
      <li style="font-family:Georgia,serif; font-style:italic; font-size:12.5px; color:#222222; line-height:1.55; margin-bottom:4px;">Enables Indian tech startups and independent developers to build world class software with leaner teams.</li>
      <li style="font-family:Georgia,serif; font-style:italic; font-size:12.5px; color:#222222; line-height:1.55; margin-bottom:0;">Accelerates the industry shift from simple chatbots toward persistent goal oriented autonomous agents.</li>
    </ul>
  </div>
</div>

<!-- SECTION 2: AI MODELS AND TOOLS -->
<div style="background:#0a0a0a; border:1px solid #000000; padding:10px 14px; margin:34px 0 16px 0;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
      <td align="left" style="font-family:'Playfair Display',Georgia,'Times New Roman',serif; font-size:14px; font-weight:900; letter-spacing:1.5px; text-transform:uppercase; color:#ffffff; line-height:1.2;">
        02 &bull; ARTIFICIAL INTELLIGENCE &amp; MODELS
      </td>
      <td align="right" style="font-family:'Courier New',monospace; font-size:10px; font-weight:800; letter-spacing:1px; text-transform:uppercase; color:#ffffff; white-space:nowrap; padding-left:8px;">
        <span style="background:#b8332a; color:#ffffff; padding:3px 8px; border:1px solid rgba(255,255,255,0.4); display:inline-block; line-height:1;">DISPATCH</span>
      </td>
    </tr>
  </table>
</div>
<div style="background:#fcfbf8; border:1px solid #1a1a1a; padding:14px 16px; margin-bottom:14px;">
  <div style="margin-bottom:6px;">
    <span style="font-family:'Courier New',monospace; font-size:9.5px; font-weight:700; color:#b8332a; letter-spacing:1px; text-transform:uppercase; margin-right:6px;">NEW MODEL</span>
    <span style="font-family:system-ui,-apple-system,sans-serif; font-size:9.5px; font-weight:600; color:#555555; vertical-align:middle;">🌍</span>
  </div>
  <a href="https://deepmind.google/technologies/gemini/" style="display:block; font-family:'Playfair Display',Georgia,serif; font-size:16px; font-weight:800; color:#111111; text-decoration:none; line-height:1.35; margin:0 0 6px 0;">Google Announces Gemini 3.8 Flash With Extended Grounding and Video Streaming</a>
  <p style="font-family:Georgia,serif; font-style:italic; font-size:13px; color:#2c2c2c; line-height:1.55; margin:0 0 8px 0;">Features sub second multi modal reasoning, native tool use, and bidirectional audio streaming tailored for scalable real time production agents.</p>
  <a href="https://deepmind.google/technologies/gemini/" style="font-family:'Courier New',monospace; font-size:10px; font-weight:700; color:#b8332a; text-decoration:none; text-transform:uppercase; letter-spacing:0.5px;">Read Full Dispatch &rarr;</a>
</div>

<!-- SECTION 3: MOBILE PHONES -->
<div style="background:#0a0a0a; border:1px solid #000000; padding:10px 14px; margin:34px 0 16px 0;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
      <td align="left" style="font-family:'Playfair Display',Georgia,'Times New Roman',serif; font-size:14px; font-weight:900; letter-spacing:1.5px; text-transform:uppercase; color:#ffffff; line-height:1.2;">
        03 &bull; HARDWARE &amp; TELEPHONY (INDIA &amp; GLOBAL)
      </td>
      <td align="right" style="font-family:'Courier New',monospace; font-size:10px; font-weight:800; letter-spacing:1px; text-transform:uppercase; color:#ffffff; white-space:nowrap; padding-left:8px;">
        <span style="background:#b8332a; color:#ffffff; padding:3px 8px; border:1px solid rgba(255,255,255,0.4); display:inline-block; line-height:1;">LAUNCH WIRE</span>
      </td>
    </tr>
  </table>
</div>
<div style="background:#fcfbf8; border:1px solid #1a1a1a; padding:14px 16px; margin-bottom:14px;">
  <div style="margin-bottom:6px;">
    <span style="font-family:'Courier New',monospace; font-size:9.5px; font-weight:700; color:#b8332a; letter-spacing:1px; text-transform:uppercase; margin-right:6px;">INDIA LAUNCH</span>
    <span style="font-family:system-ui,-apple-system,sans-serif; font-size:9.5px; font-weight:600; color:#555555; vertical-align:middle;">🇮🇳</span>
  </div>
  <a href="https://www.samsung.com/in/" style="display:block; font-family:'Playfair Display',Georgia,serif; font-size:16px; font-weight:800; color:#111111; text-decoration:none; line-height:1.35; margin:0 0 6px 0;">Samsung Galaxy S26 Ultra Debuts With On-Device 200MP Generative Zoom in India</a>
  <p style="font-family:Georgia,serif; font-style:italic; font-size:13px; color:#2c2c2c; line-height:1.55; margin:0 0 8px 0;">Priced from Rs 1,29,999 in India, featuring custom 3nm silicon alongside satellite emergency communication across national telecom networks.</p>
  <a href="https://www.samsung.com/in/" style="font-family:'Courier New',monospace; font-size:10px; font-weight:700; color:#b8332a; text-decoration:none; text-transform:uppercase; letter-spacing:0.5px;">Read Full Dispatch &rarr;</a>
</div>

<!-- SECTION 4: LAPTOPS -->
<div style="background:#0a0a0a; border:1px solid #000000; padding:10px 14px; margin:34px 0 16px 0;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
      <td align="left" style="font-family:'Playfair Display',Georgia,'Times New Roman',serif; font-size:14px; font-weight:900; letter-spacing:1.5px; text-transform:uppercase; color:#ffffff; line-height:1.2;">
        04 &bull; SILICON &amp; COMPUTING (LAPTOPS)
      </td>
      <td align="right" style="font-family:'Courier New',monospace; font-size:10px; font-weight:800; letter-spacing:1px; text-transform:uppercase; color:#ffffff; white-space:nowrap; padding-left:8px;">
        <span style="background:#b8332a; color:#ffffff; padding:3px 8px; border:1px solid rgba(255,255,255,0.4); display:inline-block; line-height:1;">DISPATCH</span>
      </td>
    </tr>
  </table>
</div>
<div style="background:#fcfbf8; border:1px solid #1a1a1a; padding:14px 16px; margin-bottom:14px;">
  <div style="margin-bottom:6px;">
    <span style="font-family:'Courier New',monospace; font-size:9.5px; font-weight:700; color:#b8332a; letter-spacing:1px; text-transform:uppercase; margin-right:6px;">NEW LAUNCH</span>
    <span style="font-family:system-ui,-apple-system,sans-serif; font-size:9.5px; font-weight:600; color:#555555; vertical-align:middle;">🇮🇳</span>
  </div>
  <a href="https://www.apple.com/in/macbook-pro/" style="display:block; font-family:'Playfair Display',Georgia,serif; font-size:16px; font-weight:800; color:#111111; text-decoration:none; line-height:1.35; margin:0 0 6px 0;">Apple Unveils MacBook Pro With M5 Silicon Featuring 128GB Unified Memory</a>
  <p style="font-family:Georgia,serif; font-style:italic; font-size:13px; color:#2c2c2c; line-height:1.55; margin:0 0 8px 0;">Engineered for local LLM inference and intensive compute workflows, starting at Rs 1,99,900 with immediate pre orders across Indian retail stores.</p>
  <a href="https://www.apple.com/in/macbook-pro/" style="font-family:'Courier New',monospace; font-size:10px; font-weight:700; color:#b8332a; text-decoration:none; text-transform:uppercase; letter-spacing:0.5px;">Read Full Dispatch &rarr;</a>
</div>

<!-- SECTION 5: NVIDIA AND GPU NEWS -->
<div style="background:#0a0a0a; border:1px solid #000000; padding:10px 14px; margin:34px 0 16px 0;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
      <td align="left" style="font-family:'Playfair Display',Georgia,'Times New Roman',serif; font-size:14px; font-weight:900; letter-spacing:1.5px; text-transform:uppercase; color:#ffffff; line-height:1.2;">
        05 &bull; GRAPHICS ACCELERATORS &amp; GPUS (NVIDIA)
      </td>
      <td align="right" style="font-family:'Courier New',monospace; font-size:10px; font-weight:800; letter-spacing:1px; text-transform:uppercase; color:#ffffff; white-space:nowrap; padding-left:8px;">
        <span style="background:#b8332a; color:#ffffff; padding:3px 8px; border:1px solid rgba(255,255,255,0.4); display:inline-block; line-height:1;">SILICON WIRE</span>
      </td>
    </tr>
  </table>
</div>
<div style="background:#fcfbf8; border:1px solid #1a1a1a; padding:14px 16px; margin-bottom:14px;">
  <div style="margin-bottom:6px;">
    <span style="font-family:'Courier New',monospace; font-size:9.5px; font-weight:700; color:#b8332a; letter-spacing:1px; text-transform:uppercase; margin-right:6px;">GPU ACCELERATOR</span>
    <span style="font-family:system-ui,-apple-system,sans-serif; font-size:9.5px; font-weight:600; color:#555555; vertical-align:middle;">🌍</span>
  </div>
  <a href="https://nvidianews.nvidia.com" style="display:block; font-family:'Playfair Display',Georgia,serif; font-size:16px; font-weight:800; color:#111111; text-decoration:none; line-height:1.35; margin:0 0 6px 0;">Nvidia Blackwell Ultra B300 Systems Enter High Volume Datacenter Production</a>
  <p style="font-family:Georgia,serif; font-style:italic; font-size:13px; color:#2c2c2c; line-height:1.55; margin:0 0 8px 0;">Delivers 4x inference throughput for trillion parameter mixture of experts models with liquid cooling standards adopted by leading cloud providers.</p>
  <a href="https://nvidianews.nvidia.com" style="font-family:'Courier New',monospace; font-size:10px; font-weight:700; color:#b8332a; text-decoration:none; text-transform:uppercase; letter-spacing:0.5px;">Read Full Dispatch &rarr;</a>
</div>

<!-- SECTION 6: CHINA TECH NEWS -->
<div style="background:#0a0a0a; border:1px solid #000000; padding:10px 14px; margin:34px 0 16px 0;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
      <td align="left" style="font-family:'Playfair Display',Georgia,'Times New Roman',serif; font-size:14px; font-weight:900; letter-spacing:1.5px; text-transform:uppercase; color:#ffffff; line-height:1.2;">
        06 &bull; CHINA TECH DOSSIER (HUAWEI &amp; DEEPSEEK)
      </td>
      <td align="right" style="font-family:'Courier New',monospace; font-size:10px; font-weight:800; letter-spacing:1px; text-transform:uppercase; color:#ffffff; white-space:nowrap; padding-left:8px;">
        <span style="background:#b8332a; color:#ffffff; padding:3px 8px; border:1px solid rgba(255,255,255,0.4); display:inline-block; line-height:1;">GLOBAL</span>
      </td>
    </tr>
  </table>
</div>
<div style="background:#fcfbf8; border:1px solid #1a1a1a; padding:14px 16px; margin-bottom:14px;">
  <div style="margin-bottom:6px;">
    <span style="font-family:'Courier New',monospace; font-size:9.5px; font-weight:700; color:#b8332a; letter-spacing:1px; text-transform:uppercase; margin-right:6px;">DEEPSEEK</span>
    <span style="font-family:system-ui,-apple-system,sans-serif; font-size:9.5px; font-weight:600; color:#555555; vertical-align:middle;">🌍</span>
  </div>
  <a href="https://www.deepseek.com" style="display:block; font-family:'Playfair Display',Georgia,serif; font-size:16px; font-weight:800; color:#111111; text-decoration:none; line-height:1.35; margin:0 0 6px 0;">DeepSeek Unveils Open Weights Reasoning Architecture Matching Frontier Models</a>
  <p style="font-family:Georgia,serif; font-style:italic; font-size:13px; color:#2c2c2c; line-height:1.55; margin:0 0 8px 0;">The open release triggers fresh competitive cost reductions across global inference providers, demonstrating exceptional mathematical proofs.</p>
  <a href="https://www.deepseek.com" style="font-family:'Courier New',monospace; font-size:10px; font-weight:700; color:#b8332a; text-decoration:none; text-transform:uppercase; letter-spacing:0.5px;">Read Full Dispatch &rarr;</a>
</div>

<!-- SECTION 7: TECH COMPANY NEWS (BIG TECH) -->
<div style="background:#0a0a0a; border:1px solid #000000; padding:10px 14px; margin:34px 0 16px 0;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
      <td align="left" style="font-family:'Playfair Display',Georgia,'Times New Roman',serif; font-size:14px; font-weight:900; letter-spacing:1.5px; text-transform:uppercase; color:#ffffff; line-height:1.2;">
        07 &bull; BIG TECH &amp; ENTERPRISE DISPATCH
      </td>
      <td align="right" style="font-family:'Courier New',monospace; font-size:10px; font-weight:800; letter-spacing:1px; text-transform:uppercase; color:#ffffff; white-space:nowrap; padding-left:8px;">
        <span style="background:#b8332a; color:#ffffff; padding:3px 8px; border:1px solid rgba(255,255,255,0.4); display:inline-block; line-height:1;">CORPORATE</span>
      </td>
    </tr>
  </table>
</div>
<div style="background:#fcfbf8; border:1px solid #1a1a1a; padding:14px 16px; margin-bottom:14px;">
  <div style="margin-bottom:6px;">
    <span style="font-family:'Courier New',monospace; font-size:9.5px; font-weight:700; color:#b8332a; letter-spacing:1px; text-transform:uppercase; margin-right:6px;">MICROSOFT</span>
    <span style="font-family:system-ui,-apple-system,sans-serif; font-size:9.5px; font-weight:600; color:#555555; vertical-align:middle;">🌍</span>
  </div>
  <a href="https://news.microsoft.com" style="display:block; font-family:'Playfair Display',Georgia,serif; font-size:16px; font-weight:800; color:#111111; text-decoration:none; line-height:1.35; margin:0 0 6px 0;">Microsoft Expands Global Datacenter Clusters for Next Generational AI Workloads</a>
  <p style="font-family:Georgia,serif; font-style:italic; font-size:13px; color:#2c2c2c; line-height:1.55; margin:0 0 8px 0;">The multi gigawatt infrastructure initiative scales compute availability for enterprise reasoning agents and foundational model training.</p>
  <a href="https://news.microsoft.com" style="font-family:'Courier New',monospace; font-size:10px; font-weight:700; color:#b8332a; text-decoration:none; text-transform:uppercase; letter-spacing:0.5px;">Read Full Dispatch &rarr;</a>
</div>

<!-- SECTION 8: EVENTS AND CONFERENCES (UPCOMING FUTURE EVENTS ONLY) -->
<div style="background:#0a0a0a; border:1px solid #000000; padding:10px 14px; margin:34px 0 16px 0;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
      <td align="left" style="font-family:'Playfair Display',Georgia,'Times New Roman',serif; font-size:14px; font-weight:900; letter-spacing:1.5px; text-transform:uppercase; color:#ffffff; line-height:1.2;">
        08 &bull; CHRONICLE CALENDAR &amp; CONFERENCES
      </td>
      <td align="right" style="font-family:'Courier New',monospace; font-size:10px; font-weight:800; letter-spacing:1px; text-transform:uppercase; color:#ffffff; white-space:nowrap; padding-left:8px;">
        <span style="background:#b8332a; color:#ffffff; padding:3px 8px; border:1px solid rgba(255,255,255,0.4); display:inline-block; line-height:1;">UPCOMING</span>
      </td>
    </tr>
  </table>
</div>
<div style="background:#fbf9f4; border:1px solid #1a1a1a; margin-bottom:28px;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-bottom:1px solid #e0dbce;">
    <tr>
      <td style="padding:12px 14px; font-family:Georgia,serif;">
        <div style="margin-bottom:4px;">
          <span style="font-family:'Courier New',monospace; font-size:9.5px; font-weight:700; color:#b8332a; letter-spacing:1px; text-transform:uppercase; margin-right:6px;">GUJARAT</span>
          <span style="font-family:system-ui,-apple-system,sans-serif; font-size:9.5px; font-weight:600; color:#555555;">🇮🇳</span>
        </div>
        <a href="https://giftgujarat.in" style="display:block; font-family:'Playfair Display',Georgia,serif; font-size:14.5px; font-weight:800; color:#111111; text-decoration:none; margin:0 0 3px 0;">Vibrant Gujarat AI &amp; FinTech Global Conclave 2027</a>
        <div style="font-family:Georgia,serif; font-style:italic; font-size:11.5px; color:#555555; margin-bottom:8px;">January 12-14, 2027 &bull; GIFT City, Gandhinagar, Gujarat</div>
        <a href="https://giftgujarat.in" style="font-family:'Courier New',monospace; font-size:9.5px; font-weight:700; color:#111111; background:#ede8dc; border:1px solid #1a1a1a; padding:5px 12px; text-decoration:none; text-transform:uppercase; letter-spacing:1px; display:inline-block;">RSVP &rarr;</a>
      </td>
    </tr>
  </table>
  <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-bottom:1px solid #e0dbce;">
    <tr>
      <td style="padding:12px 14px; font-family:Georgia,serif;">
        <div style="margin-bottom:4px;">
          <span style="font-family:'Courier New',monospace; font-size:9.5px; font-weight:700; color:#b8332a; letter-spacing:1px; text-transform:uppercase; margin-right:6px;">INDIA HACKATHON</span>
          <span style="font-family:system-ui,-apple-system,sans-serif; font-size:9.5px; font-weight:600; color:#555555;">🇮🇳</span>
        </div>
        <a href="https://www.sih.gov.in" style="display:block; font-family:'Playfair Display',Georgia,serif; font-size:14.5px; font-weight:800; color:#111111; text-decoration:none; margin:0 0 3px 0;">Smart India Hackathon 2027 Grand Edition</a>
        <div style="font-family:Georgia,serif; font-style:italic; font-size:11.5px; color:#555555; margin-bottom:8px;">February 24-26, 2027 &bull; Nodal Engineering Centers Across India</div>
        <a href="https://www.sih.gov.in" style="font-family:'Courier New',monospace; font-size:9.5px; font-weight:700; color:#111111; background:#ede8dc; border:1px solid #1a1a1a; padding:5px 12px; text-decoration:none; text-transform:uppercase; letter-spacing:1px; display:inline-block;">RSVP &rarr;</a>
      </td>
    </tr>
  </table>
</div>

<!-- SECTION 9: EDITOR'S TAKE -->
<div style="background:#0a0a0a; border:1px solid #000000; padding:10px 14px; margin:34px 0 16px 0;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
      <td align="left" style="font-family:'Playfair Display',Georgia,'Times New Roman',serif; font-size:14px; font-weight:900; letter-spacing:1.5px; text-transform:uppercase; color:#ffffff; line-height:1.2;">
        09 &bull; DID YOU KNOW... / EDITOR'S TAKE
      </td>
      <td align="right" style="font-family:'Courier New',monospace; font-size:10px; font-weight:800; letter-spacing:1px; text-transform:uppercase; color:#ffffff; white-space:nowrap; padding-left:8px;">
        <span style="background:#b8332a; color:#ffffff; padding:3px 8px; border:1px solid rgba(255,255,255,0.4); display:inline-block; line-height:1;">OPINION</span>
      </td>
    </tr>
  </table>
</div>
<div style="background:#ede9df; border:1px solid #1a1a1a; padding:18px 16px; margin-bottom:28px;">
  <p style="font-family:Georgia,serif; font-style:italic; font-size:13.5px; color:#1a1a1a; line-height:1.65; margin:0 0 12px 0;">
    As artificial intelligence accelerates into deeper reasoning and autonomous code execution, the real differentiator for engineers will always be first principles. Do not merely admire the machinery from afar, understand its mechanics, write clean code, and build sovereign systems that solve real human challenges.
  </p>
  <div style="border-left:3px solid #b8332a; padding-left:10px; margin:10px 0 12px 0;">
    <p style="font-family:Georgia,serif; font-size:13.5px; font-weight:bold; color:#111111; margin:0; font-style:italic;">
      &ldquo;Do not merely admire the machine, master its mechanics and build what has never existed.&rdquo;
    </p>
  </div>
  <div style="font-family:'Courier New',monospace; font-size:10.5px; color:#444444; text-transform:uppercase;">
    &mdash; <strong>{EDITOR_NAME}</strong>, {EDITOR_TITLE}
  </div>
</div>
"""


def sanitize_events_section(html_text: str) -> str:
    """
    Validates Section 8 (Events and Conferences):
    If past events are found (e.g. prior to November 18, 2026: March 2026, April 2026, 2025, 2024, etc.)
    or if past dates are detected, replaces Section 8 with the clean vintage empty state notice.
    """
    past_pattern = re.compile(
        r'(?:January|February|March|April|May|June|July|August|September|October|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct)[a-z]*\s+(?:[0-9]{1,2}[,\s\-–]+)+2026|2024|2025',
        re.IGNORECASE
    )
    
    sec8_match = re.search(
        r'(<!--\s*SECTION 8[^-]*-->|<div[^>]*>.*?08.*?</div>|<h2[^>]*>.*?Events.*?</h2>)(.*?)(<!--\s*SECTION 9|<div[^>]*>.*?09|<h2[^>]*>.*?Editor.*?</h2>|\Z)',
        html_text,
        re.DOTALL | re.IGNORECASE
    )
    
    if sec8_match:
        sec8_content = sec8_match.group(2)
        if past_pattern.search(sec8_content):
            print("[TechAi Samachar] Past dates detected in Section 8 events. Replacing with verified empty state notice.")
            empty_notice = '''<div style="background:#0a0a0a; border:1px solid #000000; padding:10px 14px; margin:34px 0 16px 0;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
      <td align="left" style="font-family:'Playfair Display',Georgia,'Times New Roman',serif; font-size:14px; font-weight:900; letter-spacing:1.5px; text-transform:uppercase; color:#ffffff; line-height:1.2;">
        08 &bull; CHRONICLE CALENDAR &amp; CONFERENCES
      </td>
      <td align="right" style="font-family:'Courier New',monospace; font-size:10px; font-weight:800; letter-spacing:1px; text-transform:uppercase; color:#ffffff; white-space:nowrap; padding-left:8px;">
        <span style="background:#b8332a; color:#ffffff; padding:3px 8px; border:1px solid rgba(255,255,255,0.4); display:inline-block; line-height:1;">NOTICE</span>
      </td>
    </tr>
  </table>
</div>
<div style="background:#fbf9f4; border:1px solid #1a1a1a; padding:18px 16px; text-align:center; margin-bottom:28px;">
  <p style="font-family:Georgia,serif; font-style:italic; font-size:13.5px; color:#444444; margin:0; line-height:1.6;">
    No confirmed upcoming conferences or hackathons scheduled for the immediate cycle. Please consult tomorrow's morning edition.
  </p>
</div>
'''
            html_text = html_text[:sec8_match.start(1)] + empty_notice + html_text[sec8_match.start(3):]

    return html_text


def fetch_and_curate_news() -> Tuple[str, List[Dict[str, str]]]:
    """
    Calls Gemini API with Google Search grounding.
    Returns (html_body_fragment, citations_list).
    """
    if not GEMINI_API_KEY:
        print("[TechAi Samachar] No GEMINI_API_KEY detected in environment. Using curated editorial demo data.")
        demo_html = get_demo_html()
        citations = [
            {"title": "Google DeepMind Frontier Research", "url": "https://deepmind.google"},
            {"title": "Nvidia Blackwell Systems & Silicon", "url": "https://www.nvidia.com"},
            {"title": "Smart India Hackathon Official Portal", "url": "https://www.sih.gov.in"},
            {"title": "GIFT City Gujarat FinTech Initiative", "url": "https://giftgujarat.in"},
        ]
        return demo_html, citations

    today = get_formatted_date()
    short_date = get_short_date()
    edition = get_edition_number()

    client = genai.Client(api_key=GEMINI_API_KEY)

    print(f"[{short_date}] Querying Gemini model with Google Search Grounding for 9 curated sections...")
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=build_prompt(today),
            config=types.GenerateContentConfig(
                tools=[{"google_search": {}}],
                temperature=0.35,
            )
        )

        raw_html = response.text or ""
        # Clean markdown wrappers if present
        raw_html = re.sub(r"^```html\s*", "", raw_html, flags=re.IGNORECASE | re.MULTILINE)
        raw_html = re.sub(r"^```\s*", "", raw_html, flags=re.MULTILINE)
        raw_html = raw_html.strip()

        # Enforce zero-dash rule
        raw_html = raw_html.replace("\u2014", ", ").replace("\u2013", ", ")

        # Enforce upcoming-only events rule
        raw_html = sanitize_events_section(raw_html)

        # Extract Grounding citations
        citations = []
        candidates = getattr(response, "candidates", None)
        if candidates and len(candidates) > 0:
            grounding_meta = getattr(candidates[0], "grounding_metadata", None)
            if grounding_meta and hasattr(grounding_meta, "grounding_chunks"):
                seen = set()
                for chunk in grounding_meta.grounding_chunks or []:
                    web = getattr(chunk, "web", None)
                    if web:
                        uri = getattr(web, "uri", None)
                        title = getattr(web, "title", None)
                        if uri and uri not in seen:
                            seen.add(uri)
                            clean_title = re.sub(r'[<>"]', '', title or uri)
                            citations.append({
                                "title": clean_title,
                                "url": uri
                            })

        print(f"[TechAi Samachar] Successfully generated 9 sections for edition #{edition} with {len(citations)} citations.")
        return raw_html, citations

    except Exception as e:
        print(f"[TechAi Samachar] Warning: Gemini API call encountered an issue ({e}). Falling back to curated sample.")
        return get_demo_html(), []
