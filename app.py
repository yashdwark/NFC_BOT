import datetime
import requests
import pytz
import threading
from flask import Flask, request, redirect

app = Flask(__name__)

# ---------------- TELEGRAM SETTINGS ----------------
BOT_TOKEN = "8448843598:AAHCEYvau9QwdU_DHAIn7zBbXMS1KBBQkOM"
CHAT_ID = "636628877"
BOT_NAME = "Tagwatchbot"

# >>> GOOGLE FORM LINK <<<
GOOGLE_FORM_LINK = "https://forms.gle/qtM8TXP21RMLgyGK9"


# ---------------- TELEGRAM SENDER (NON-BLOCKING) ----------------
def send_telegram_msg(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        payload = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }

        requests.post(url, json=payload, timeout=6)

    except Exception as e:
        print("Telegram Error:", e)


# run telegram in background (IMPORTANT — prevents 502 error)
def send_async(message):
    threading.Thread(target=send_telegram_msg, args=(message,)).start()


# ===== HOME PAGE =====
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
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.datetime.now(ist).strftime("%I:%M %p | %d %b %Y")

    # Device detection
    user_agent = request.headers.get('User-Agent', '').lower()

    if "iphone" in user_agent:
        device = "🍏 iPhone"
    elif "android" in user_agent:
        device = "🤖 Android"
    elif "windows" in user_agent:
        device = "💻 Windows PC"
    elif "mac" in user_agent:
        device = "💻 Mac"
    else:
        device = "📱 Unknown Device"

    # ================= REAL CLIENT IP (IMPORTANT FIX) =================
    # Works with NGINX reverse proxy
    if request.headers.get("X-Forwarded-For"):
        real_ip = request.headers.get("X-Forwarded-For").split(",")[0].strip()
    else:
        real_ip = request.remote_addr

    print("SCAN FROM:", real_ip, "AT:", now)

    # Telegram message
    msg = f"""
<b>🔔 {BOT_NAME} Alert!</b>
━━━━━━━━━━━━━━━
📍 <b>Status:</b> NFC Tag Scanned
⏰ <b>Time:</b> {now}
📱 <b>Device:</b> {device}
🌐 <b>IP:</b> {real_ip}
━━━━━━━━━━━━━━━
"""

    # send in background (VERY IMPORTANT)
    send_async(msg)

    # Redirect to Google Form
    return redirect(GOOGLE_FORM_LINK)


# ================= THANK YOU PAGE =================
@app.route('/thanks')
def thanks():
    return """
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <script>
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
    app.run(host="0.0.0.0", port=80)