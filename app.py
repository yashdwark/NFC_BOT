import datetime
import requests
from flask import Flask, request, redirect

app = Flask(__name__)

# ---------------- TELEGRAM SETTINGS ----------------
BOT_TOKEN = "8448843598:AAHCEYvau9QwdU_DHAIn7zBbXMS1KBBQkOM"
CHAT_ID = "636628877"
BOT_NAME = "Tagwatchbot"

# >>>>>>>>>>>>>>> ADD YOUR GOOGLE FORM LINK HERE <<<<<<<<<<<<<<<<<
GOOGLE_FORM_LINK = "https://forms.gle/qtM8TXP21RMLgyGK9"
# Example:
# GOOGLE_FORM_LINK = "https://forms.gle/AbCdEf12345"


# Send message to Telegram
def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print("Telegram Error:", e)

# ===== HOME PAGE (when someone opens main link) =====
@app.route('/')
def home():
    return """
    <h2 style="font-family:Arial;text-align:center;margin-top:80px;">
    NFC Bot is running successfully ✅
    </h2>
    """

# ================= NFC SCAN PAGE =================
# THIS IS THE LINK YOU WILL WRITE INTO NFC
@app.route('/scan')
def scan_handler():

    # Time
    now = datetime.datetime.now().strftime("%I:%M %p | %d %b %Y")

    # Device detection
    user_agent = request.headers.get('User-Agent', 'Unknown')

    if "iPhone" in user_agent:
        device = "🍏 iPhone"
    elif "Android" in user_agent:
        device = "🤖 Android"
    else:
        device = "💻 Computer"

    # Telegram message
    msg = f"""
<b>🔔 {BOT_NAME} Alert!</b>
━━━━━━━━━━━━━━━
📍 <b>Status:</b> NFC Tag Scanned
⏰ <b>Time:</b> {now}
📱 <b>Device:</b> {device}
🌐 <b>IP:</b> {request.remote_addr}
━━━━━━━━━━━━━━━
"""

    send_telegram_msg(msg)

    # 🔴 DIRECTLY OPEN GOOGLE FORM
    return redirect(GOOGLE_FORM_LINK)


# ================= BROCHURE DOWNLOAD PAGE =================
@app.route('/thanks')
def thanks():
    return """
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <script>
        // Auto download PDF
        window.onload = function(){
            window.location.href = "https://drive.google.com/uc?export=download&id=14fJEVtIL_TQHt-uQpJZUiu0iW2rDPWxM";
        }
        </script>

    </head>

    <body style="text-align:center;padding-top:90px;font-family:Arial;background:#f2f4f8;">
        <h2>✅ We will get back to you soon</h2>
        <p>Your brochure is downloading...</p>
    </body>
    </html>
    """


# ================= SERVER START =================
if __name__ == '__main__':
    print("Server running...")
    app.run(host="0.0.0.0", port=5000)