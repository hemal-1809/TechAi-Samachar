require('dotenv').config();
const { GoogleGenAI } = require('@google/genai');
const nodemailer = require('nodemailer');

const requiredEnvVars = ['GEMINI_API_KEY', 'EMAIL_USER', 'EMAIL_PASS', 'EMAIL_TO'];
const missingVars = requiredEnvVars.filter(v => !process.env[v]);
if (missingVars.length > 0) {
  console.error('Missing required environment variables:');
  missingVars.forEach(v => console.error('  ' + v));
  process.exit(1);
}

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

function getFormattedDate() {
  return new Date().toLocaleDateString('en-US', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
  });
}
function getShortDate() {
  return new Date().toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', year: 'numeric',
  });
}
function getEditionNumber() {
  const start = new Date('2026-01-01');
  const diff = Math.floor((new Date() - start) / (1000 * 60 * 60 * 24));
  return diff + 1;
}

// ─── PREMIUM GEMINI PROMPT WITH HYBRID RESPONSIVE BLUEPRINTS ────────────────
function buildPrompt(today) {
  return `
You are "TechAi Samachar", a world-class AI tech journalist writing a premium daily newsletter.
Today is ${today}.

Search the web and find the absolute latest AI and technology news from the past 24 to 48 hours.

TONE:
- Write like a brilliant human journalist. Warm, exciting, conversational.
- Zero dashes anywhere. Use commas, periods, or "and" instead.
- Short punchy sentences. Make readers feel like they are reading a friend's insider update.
- Every headline MUST be a real clickable <a> link pointing to the actual source URL.

OUTPUT FORMAT:
Return a single HTML fragment only. No <html>, <head>, or <body> tags. Just the inner content content elements.
Use ONLY inline CSS. No <style> blocks. This is for cross-platform email client rendering.

FOLLOW THIS EXACT SECTION ORDER AND MOBILE-FIRST STRUCTURAL BLOCKS:

============================================================
SECTION 1: BREAKING NEWS
============================================================
The single biggest story right now.

Wrap entire section in:
<div style="margin-bottom:32px; border-radius:16px; overflow:hidden; border:1px solid #eef0f3; box-shadow:0 4px 20px rgba(0,0,0,0.03);">

Inside:
<div style="height:6px; background:linear-gradient(90deg,#ef4444,#f97316);"></div>
<div style="padding:24px; background:#ffffff;">
  <div style="margin-bottom:12px;"><span style="display:inline-block; background:#ef4444; color:#ffffff; font-size:10px; font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; padding:5px 12px; border-radius:30px; box-shadow:0 2px 4px rgba(239,68,68,0.2);">BREAKING</span></div>
  <a href="[REAL_URL]" style="display:block; font-family:Georgia,serif; font-size:22px; font-weight:800; color:#111827; text-decoration:none; line-height:1.35; margin:0 0 14px 0;">[Headline]</a>
  <p style="font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif; font-size:14.5px; color:#4b5563; line-height:1.75; margin:0 0 20px 0;">[3 to 4 sentences summaries]</p>
  <div style="background:#fff7ed; border-left:4px solid #f97316; border-radius:4px 12px 12px 4px; padding:18px; margin-top:4px;">
    <p style="font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:1px; color:#c2410c; margin:0 0 10px 0;">Why This Matters</p>
    <ul style="margin:0; padding-left:18px;">
      <li style="font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif; font-size:13.5px; color:#4b5563; line-height:1.7; margin-bottom:6px;">[Insight 1]</li>
      <li style="font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif; font-size:13.5px; color:#4b5563; line-height:1.7; margin-bottom:6px;">[Insight 2]</li>
      <li style="font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif; font-size:13.5px; color:#4b5563; line-height:1.7; margin-bottom:0;">[Insight 3]</li>
    </ul>
  </div>
</div>
</div>

============================================================
SECTION 2: NEW AI TOOLS AND PLATFORMS
============================================================
2 to 3 newly launched AI tools or platforms.

Section header style:
<h2 style="font-family:Georgia,serif; font-size:19px; font-weight:800; color:#111827; margin:40px 0 20px 0; padding-bottom:12px; border-bottom:2px solid #f3f4f6;">
  <span style="display:inline-block; background:#059669; color:#ffffff; width:30px; height:30px; border-radius:8px; text-align:center; line-height:30px; font-size:15px; margin-right:8px; vertical-align:middle;">🛠</span>
  <span style="vertical-align:middle;">New AI Tools and Platforms</span>
</h2>

Each tool card MUST use a fluid, non-flex block structure that safely layout-collapses vertically on mobile devices:
<div style="padding:20px; background:#ffffff; border:1px solid #f3f4f6; border-radius:14px; margin-bottom:16px; box-shadow:0 4px 12px rgba(0,0,0,0.015);">
  <div style="margin-bottom:10px;">
    <span style="display:inline-block; background:#ecfdf5; color:#059669; border:1px solid rgba(5,150,105,0.25); font-size:9px; font-family:system-ui,-apple-system,sans-serif; font-weight:700; text-transform:uppercase; letter-spacing:1px; padding:3px 10px; border-radius:30px; margin-right:8px; vertical-align:middle;">[NEW TOOL or PLATFORM or OPEN SOURCE]</span>
    <span style="font-size:18px; vertical-align:middle; display:inline-block; margin-right:6px;">[relevant emoji]</span>
  </div>
  <a href="[REAL_URL]" style="display:block; font-family:Georgia,serif; font-size:16px; font-weight:700; color:#111827; text-decoration:none; line-height:1.45; margin:0 0 8px 0;">[Tool Name and Headline]</a>
  <p style="font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif; font-size:13.5px; color:#4b5563; line-height:1.7; margin:0 0 12px 0;">[2 to 3 sentence summary. Who built it? What does it do?]</p>
  <a href="[REAL_URL]" style="font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif; font-size:13px; font-weight:700; color:#059669; text-decoration:none; display:inline-block;">Read the full story &rarr;</a>
</div>

============================================================
SECTION 3: AI MODELS AND UPDATES
============================================================
2 to 3 new model releases or major updates.

Same section header style but with purple color elements:
Header Icon Background: #4f46e5 (use brain emoji 🧠)

Each model card layout matches Section 2 tools layout precisely but with these custom properties:
- Card Top Header Badge style: background:#eef2ff; color:#4f46e5; border:1px solid rgba(79,70,229,0.25); with model system like [GEMINI] [CLAUDE] [GPT] [LLAMA]
- Read more link color style: #4f46e5

============================================================
SECTION 4: BEYOND AI: TECH WORLD ROUNDUP
============================================================
2 to 3 non-AI tech stories (Hardware, chips, market updates, workspace shifts).

Section header style matching previous sections with amber color #d97706 and globe emoji 🌐

Each item row card element:
<div style="padding:18px; background:#fffdf5; border:1px solid #fef3c7; border-radius:12px; margin-bottom:14px; box-shadow:0 4px 12px rgba(217,119,6,0.02);">
  <div style="margin-bottom:10px;">
    <span style="display:inline-block; background:#fef3c7; color:#92400e; border:1px solid rgba(146,64,14,0.25); font-size:9px; font-family:system-ui,-apple-system,sans-serif; font-weight:700; letter-spacing:1px; text-transform:uppercase; padding:3px 10px; border-radius:30px; margin-right:8px; vertical-align:middle;">[HARDWARE or STARTUP or CHIPS or INDUSTRY etc]</span>
    <span style="font-size:16px; vertical-align:middle; display:inline-block;">[relevant emoji]</span>
  </div>
  <a href="[REAL_URL]" style="display:block; font-family:Georgia,serif; font-size:15px; font-weight:700; color:#111827; text-decoration:none; line-height:1.45; margin:0 0 6px 0;">[Headline]</a>
  <p style="font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif; font-size:13.5px; color:#4b5563; line-height:1.65; margin:0 0 10px 0;">[1 to 2 sentence summary]</p>
  <a href="[REAL_URL]" style="font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif; font-size:13px; font-weight:700; color:#92400e; text-decoration:none; display:inline-block;">Read more &rarr;</a>
</div>

============================================================
SECTION 5: EVENTS AND CONFERENCES
============================================================
2 to 3 upcoming or recent tech events.

Section header with calendar emoji 📅 and blue color #2563eb.

Wrap entire block container structure in:
<div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:14px; overflow:hidden; margin-bottom:36px; box-shadow:0 4px 12px rgba(0,0,0,0.01);">

Each single event element inside MUST be constructed using a robust hybrid table element layout to prevent text crowding on smartphones:
<table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-bottom:1px solid #e2e8f0;">
  <tr>
    <td style="padding:16px 20px; font-family:system-ui,-apple-system,sans-serif;">
      <div style="display:inline-block; width:100%; max-width:400px; vertical-align:middle; margin-bottom:12px;">
        <a href="[REAL_URL]" style="display:block; font-family:Georgia,serif; font-size:15px; font-weight:700; color:#1e3a8a; text-decoration:none; margin:0 0 4px 0;">[Event Name]</a>
        <p style="font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif; font-size:12.5px; color:#3b82f6; font-weight:600; margin:0;">[Date] &bull; [Location or Online]</p>
      </div>
      <div style="display:inline-block; width:100%; max-width:120px; text-align:left; vertical-align:middle;">
        <a href="[REAL_URL]" style="display:inline-block; font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif; font-size:12px; font-weight:700; color:#ffffff; background:#2563eb; padding:8px 18px; border-radius:30px; text-decoration:none; text-align:center; box-shadow:0 2px 4px rgba(37,99,235,0.2);">Register &rarr;</a>
      </div>
      </td>
  </tr>
</table>
</div>

============================================================
SECTION 6: EDITOR'S TAKE
============================================================
3 to 4 lines of personal commentary from the editor.

<div style="background:#fdfeff; border:1px solid #f3e8ff; border-left:5px solid #7c3aed; border-radius:4px 16px 16px 4px; padding:20px; margin-bottom:36px; box-shadow:0 4px 16px rgba(124,58,237,0.02);">
  <p style="font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:1.5px; color:#7c3aed; margin:0 0 12px 0;">Editor's Take</p>
  <p style="font-family:Georgia,serif; font-size:15.5px; color:#3b0764; line-height:1.8; margin:0 0 16px 0; font-style:italic;">[First person editorial commentary targeting Indian tech students and developers.]</p>
  
  <div>
    <div style="display:inline-block; width:36px; height:36px; border-radius:50%; background:#f3e8ff; text-align:center; line-height:36px; font-size:18px; margin-right:10px; vertical-align:middle;">✍️</div>
    <div style="display:inline-block; vertical-align:middle;">
      <p style="font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif; font-size:13px; font-weight:700; color:#4c1d95; margin:0;">Hemal Mistry</p>
      <p style="font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif; font-size:11px; color:#7c3aed; margin:2px 0 0 0;">Editor, TechAi Samachar</p>
    </div>
  </div>
</div>

ABSOLUTE MANIFEST RULES:
- All news items MUST be strictly grounded from actual current web searches.
- ZERO dashes inside the text content. Replace with commas or alternative joining words.
- Return raw HTML fragment only. Do not enclose content with markdown wrappers or backtick definitions.
`;
}

// ─── FULLY RESPONSIVE EMAIL WRAPPER ─────────────────────────────────────────
function buildEmailHTML(emailHtmlBody, citationsHtml, today, shortDate, edition) {
  const heroImages = [
    'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=640&h=240&q=80',
    'https://images.unsplash.com/photo-1639762681485-074b7f938ba0?auto=format&fit=crop&w=640&h=240&q=80',
    'https://images.unsplash.com/photo-1634017839464-5c339ebe3cb4?auto=format&fit=crop&w=640&h=240&q=80'
  ];
  const midImages = [
    'https://images.unsplash.com/photo-1607799279861-4dd421887fb3?auto=format&fit=crop&w=568&h=120&q=80',
    'https://images.unsplash.com/photo-1542831371-29b0f74f9713?auto=format&fit=crop&w=568&h=120&q=80'
  ];
  
  const dayOfWeek = new Date().getDay();
  const heroImg = heroImages[dayOfWeek % heroImages.length];
  const midImg  = midImages[dayOfWeek % midImages.length];

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TechAi Samachar, ${shortDate}</title>
</head>
<body style="margin:0;padding:0;background-color:#f8fafc;font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;">

<table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color:#f8fafc;padding:20px 8px;">
<tr>
  <td align="center">
    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:640px;background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,0.04);border:1px solid #e2e8f0;">

      <tr><td style="height:5px;background:linear-gradient(90deg,#ef4444 0%,#f97316 33%,#4f46e5 66%,#059669 100%);"></td></tr>

      <tr>
        <td style="padding:28px 24px 0 24px;text-align:center;">
          <table border="0" cellpadding="0" cellspacing="0" width="100%">
            <tr>
              <td align="left" style="font-family:system-ui,-apple-system,sans-serif;font-size:10px;color:#64748b;text-transform:uppercase;letter-spacing:1px;font-weight:700;">Edition #${edition}</td>
              <td align="center" style="font-family:system-ui,-apple-system,sans-serif;font-size:10px;color:#64748b;text-transform:uppercase;letter-spacing:1px;font-weight:700;">Daily Intelligence</td>
              <td align="right" style="font-family:system-ui,-apple-system,sans-serif;font-size:10px;color:#64748b;text-transform:uppercase;letter-spacing:1px;font-weight:700;">Free Insight</td>
            </tr>
          </table>
          <h1 style="margin:20px 0 6px 0;font-family:Georgia,'Times New Roman',serif;font-size:38px;font-weight:900;color:#0f172a;letter-spacing:-1px;line-height:1.1;">
            TechAi Samachar
          </h1>
          <p style="margin:0 0 8px 0;font-family:Georgia,'Times New Roman',serif;font-size:13px;color:#64748b;font-style:italic;letter-spacing:0.3px;">
            Your Trusted Daily AI and Technology Newspaper
          </p>
          <div style="font-family:system-ui,-apple-system,sans-serif;font-size:11px;color:#1e293b;font-weight:600;padding:6px 0 16px 0;letter-spacing:0.5px;text-transform:uppercase;border-bottom:1px solid #f1f5f9;">
            ${today}
          </div>
        </td>
      </tr>

      <tr>
        <td style="padding:16px 24px 0 24px;">
          <div style="border-radius:12px;overflow:hidden;box-shadow:0 4px 15px rgba(0,0,0,0.05);background-color:#0f172a;">
            <img src="${heroImg}" alt="TechAi Samachar Core Context" width="592" style="width:100%;max-width:592px;height:auto;display:block;border:0;" />
            <div style="background:rgba(15,23,42,0.9);padding:10px 16px;">
              <span style="font-family:system-ui,-apple-system,sans-serif;font-size:11px;color:#f8fafc;letter-spacing:0.5px;font-weight:500;">
                &#128248; Today's top stories curated by AI &nbsp;|&nbsp; ${shortDate}
              </span>
            </div>
          </div>
        </td>
      </tr>

      <tr>
        <td style="padding:16px 24px 0 24px;">
          <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background:#0f172a;border-radius:10px;overflow:hidden;">
            <tr>
              <td style="padding:4px 0;text-align:center;">
                <div style="display:inline-block; width:100%; max-width:130px; padding:10px 0; font-family:system-ui,-apple-system,sans-serif; font-size:10px; color:#ffffff; font-weight:700; text-transform:uppercase; letter-spacing:1px;">
                  &#128680; Breaking
                </div>
                <div style="display:inline-block; width:100%; max-width:130px; padding:10px 0; font-family:system-ui,-apple-system,sans-serif; font-size:10px; color:#94a3b8; font-weight:600; text-transform:uppercase; letter-spacing:1px;">
                  &#128736; AI Tools
                </div>
                <div style="display:inline-block; width:100%; max-width:130px; padding:10px 0; font-family:system-ui,-apple-system,sans-serif; font-size:10px; color:#94a3b8; font-weight:600; text-transform:uppercase; letter-spacing:1px;">
                  &#129504; Models
                </div>
                <div style="display:inline-block; width:100%; max-width:130px; padding:10px 0; font-family:system-ui,-apple-system,sans-serif; font-size:10px; color:#94a3b8; font-weight:600; text-transform:uppercase; letter-spacing:1px;">
                  &#127760; Tech World
                </div>
                </td>
            </tr>
          </table>
        </td>
      </tr>

      <tr>
        <td style="padding:16px 24px 8px 24px;">
          <div style="background:#f8fafc;padding:14px 18px;border-radius:10px;border:1px solid #f1f5f9;">
            <p style="margin:0;font-family:system-ui,-apple-system,sans-serif;font-size:13.5px;color:#475569;line-height:1.6;">
              Good morning! &#9728;&#65039; Here is everything that happened in AI and technology over the last 24 hours, beautifully curated and summarized so you can jumpstart your day fully informed.
            </p>
          </div>
        </td>
      </tr>

      <tr>
        <td style="padding:8px 24px;">
          ${emailHtmlBody}
        </td>
      </tr>

      <tr>
        <td style="padding:8px 24px 16px 24px;">
          <div style="border-radius:12px;overflow:hidden;box-shadow:0 4px 12px rgba(0,0,0,0.03);background-color:#0f172a;">
            <img src="${midImg}" alt="Developer Context Anchor" width="592" style="width:100%;max-width:592px;height:auto;display:block;border:0;" />
            <div style="background:rgba(15,23,42,0.8);padding:12px 18px;">
              <span style="font-family:Georgia,serif;font-size:12.5px;color:#ffffff;font-style:italic;opacity:0.95;">
                Stay curious. Build things. The future belongs to those who understand it. &#128161;
              </span>
            </div>
          </div>
        </td>
      </tr>

      <tr>
        <td style="padding:0 24px 20px 24px;">
          <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:14px;overflow:hidden;">
            <tr>
              <td style="padding:12px 4px; text-align:center;">
                <div style="display:inline-block; width:100%; max-width:130px; vertical-align:middle; padding:8px 0;">
                  <div style="font-family:Georgia,serif;font-size:22px;font-weight:800;color:#ef4444;">24</div>
                  <div style="font-family:system-ui,-apple-system,sans-serif;font-size:9px;color:#64748b;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-top:2px;">Stories</div>
                </div>
                <div style="display:inline-block; width:100%; max-width:130px; vertical-align:middle; padding:8px 0;">
                  <div style="font-family:Georgia,serif;font-size:22px;font-weight:800;color:#059669;">6</div>
                  <div style="font-family:system-ui,-apple-system,sans-serif;font-size:9px;color:#64748b;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-top:2px;">AI Tools</div>
                </div>
                <div style="display:inline-block; width:100%; max-width:130px; vertical-align:middle; padding:8px 0;">
                  <div style="font-family:Georgia,serif;font-size:22px;font-weight:800;color:#4f46e5;">3</div>
                  <div style="font-family:system-ui,-apple-system,sans-serif;font-size:9px;color:#64748b;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-top:2px;">Models</div>
                </div>
                <div style="display:inline-block; width:100%; max-width:130px; vertical-align:middle; padding:8px 0;">
                  <div style="font-family:Georgia,serif;font-size:22px;font-weight:800;color:#f97316;">5</div>
                  <div style="font-family:system-ui,-apple-system,sans-serif;font-size:9px;color:#64748b;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-top:2px;">Events</div>
                </div>
                </td>
            </tr>
          </table>
        </td>
      </tr>

      <tr>
        <td style="padding:0 24px 28px 24px;">
          ${citationsHtml}
        </td>
      </tr>

      <tr>
        <td style="border-top:1px solid #e2e8f0;padding:28px 24px;text-align:center;background:#fafafa;">
          <h3 style="margin:0 0 4px 0;font-family:Georgia,'Times New Roman',serif;font-size:20px;font-weight:900;color:#0f172a;letter-spacing:-0.5px;">
            TechAi Samachar
          </h3>
          <p style="margin:0 0 4px 0;font-family:system-ui,-apple-system,sans-serif;font-size:11px;color:#94a3b8;font-weight:600;letter-spacing:1px;text-transform:uppercase;">
            Created by Hemal Mistry
          </p>
          <div style="width:40px;height:3px;background:linear-gradient(90deg,#ef4444,#f97316);border-radius:2px;margin:12px auto;"></div>
          <div style="border-top:1px solid #f1f5f9;margin:14px auto;width:50%;"></div>

          <table border="0" cellpadding="0" cellspacing="0" style="margin:0 auto;">
            <tr>
              <td style="padding:0 8px;">
                <a href="#" style="color:#ef4444;font-size:11px;text-decoration:none;font-weight:700;font-family:system-ui,-apple-system,sans-serif;">Unsubscribe</a>
              </td>
              <td style="color:#cbd5e1;font-size:11px;">|</td>
              <td style="padding:0 8px;">
                <a href="#" style="color:#ef4444;font-size:11px;text-decoration:none;font-weight:700;font-family:system-ui,-apple-system,sans-serif;">Share Story</a>
              </td>
              <td style="color:#cbd5e1;font-size:11px;">|</td>
              <td style="padding:0 8px;">
                <a href="#" style="color:#ef4444;font-size:11px;text-decoration:none;font-weight:700;font-family:system-ui,-apple-system,sans-serif;">Feedback</a>
              </td>
            </tr>
          </table>

          <p style="margin:18px 0 0 0;font-family:system-ui,-apple-system,sans-serif;font-size:11px;color:#94a3b8;line-height:1.6;">
            Delivered every morning at 8:30 AM IST &nbsp;&#183;&nbsp; Powered by Gemini AI + Google Search<br/>
            ${today}<br/>
            You are receiving this because you subscribed to TechAi Samachar.
          </p>
        </td>
      </tr>

      <tr><td style="height:5px;background:linear-gradient(90deg,#059669 0%,#4f46e5 40%,#f97316 70%,#ef4444 100%);"></td></tr>

    </table>
  </td>
</tr>
</table>

</body>
</html>`;
}

// ─── MAIN COMPILING WORKER AGENT ───────────────────────────────────────────
async function runDailyAIAgent() {
  const today     = getFormattedDate();
  const shortDate = getShortDate();
  const edition   = getEditionNumber();

  console.log('[' + new Date().toISOString() + '] TechAi Samachar Agent launching layout engines...');
  console.log('Date Target: ' + today + ' | Edition Reference: #' + edition);

  try {
    console.log('Dispatching request to Gemini core model with search tools...');

    const response = await ai.models.generateContent({
      model: 'gemini-2.5-flash',
      contents: buildPrompt(today),
      config: {
        tools: [{ googleSearch: {} }],
        temperature: 0.35,
      },
    });

    let emailHtmlBody = response.text || '';
    emailHtmlBody = emailHtmlBody.replace(/^```html\s*/i, '').replace(/```\s*$/i, '').trim();
    emailHtmlBody = emailHtmlBody.replace(/\u2014/g, ', ').replace(/\u2013/g, ', ');
    console.log('Main structural article chunks successfully created.');

    // Assemble References
    const groundingMetadata = response.candidates?.[0]?.groundingMetadata;
    let citationsHtml = '';

    if (groundingMetadata?.groundingChunks) {
      const uniqueSources = new Map();
      groundingMetadata.groundingChunks.forEach(chunk => {
        if (chunk.web?.uri && chunk.web?.title) {
          const url   = chunk.web.uri;
          const title = chunk.web.title.replace(/[<>"]/g, '');
          if (!uniqueSources.has(url)) uniqueSources.set(url, title);
        }
      });

      if (uniqueSources.size > 0) {
        let sourceItems = '';
        let idx = 0;
        for (const [url, title] of uniqueSources.entries()) {
          idx++;
          const bg = idx % 2 === 0 ? '#ffffff' : '#f8fafc';
          sourceItems += `
            <tr>
              <td style="padding:10px 14px;font-size:12.5px;color:#334155;background:${bg};border-bottom:1px solid #f1f5f9;line-height:1.4;font-family:system-ui,-apple-system,sans-serif;">
                <span style="color:#ef4444;font-weight:700;margin-right:4px;">${idx}.</span>
                <a href="${url}" target="_blank" style="color:#0f172a;text-decoration:none;font-weight:500;">${title}</a>
              </td>
            </tr>`;
        }
        citationsHtml = `
          <div style="margin-top:20px;">
            <h3 style="font-family:Georgia,serif;font-size:16px;font-weight:800;color:#0f172a;margin:0 0 10px 0;padding-bottom:8px;border-bottom:2px solid #f1f5f9;">
              &#128279; Sources and References
            </h3>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-radius:10px;border:1px solid #e2e8f0;overflow:hidden;">
              ${sourceItems}
            </table>
          </div>`;
        console.log('Compiled ' + uniqueSources.size + ' source URLs.');
      }
    }

    // Build Fluid HTML Frame
    const completeEmailHtml = buildEmailHTML(emailHtmlBody, citationsHtml, today, shortDate, edition);

    console.log('Connecting to SMTP relay network server...');
    const transporter = nodemailer.createTransport({
      host: process.env.EMAIL_HOST || 'smtp.gmail.com',
      port: parseInt(process.env.EMAIL_PORT || '587', 10),
      secure: false,
      auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASS,
      },
    });

    const recipientEmails = process.env.EMAIL_TO
      .split(',').map(e => e.trim()).filter(e => e.length > 0).join(', ');

    await transporter.sendMail({
      from: '"TechAi Samachar" <' + process.env.EMAIL_USER + '>',
      to: recipientEmails,
      subject: '🗞️ TechAi Samachar, ' + shortDate + ' — Your Daily AI and Tech Newspaper',
      html: completeEmailHtml,
    });

    console.log('✅ Responsive newsletter delivered: ' + recipientEmails);
    return true;

  } catch (error) {
    console.error('System Architecture Exception on TechAi Samachar compiler:');
    console.error(error);
    process.exit(1);
  }
}

runDailyAIAgent();