import datetime
import requests
from flask import Flask, request

app = Flask(__name__)


# --- YOUR BOT CREDENTIALS ---
BOT_TOKEN = "8448843598:AAHCEYvau9QwdU_DHAIn7zBbXMS1KBBQkOM"
CHAT_ID = "636628877" # <--- Paste your ID here
BOT_NAME = "Tagwatchbot"  # Or whichever name you chose!

def send_telegram_msg(message):
    # FIXED: Used the BOT_TOKEN variable here instead of the raw number
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID, 
        "text": message, 
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload)
        # Optional: Print response to debug why it might fail
        print(f"Telegram API Response: {response.status_code} - {response.text}")
        return response.json()
    except Exception as e:
        print(f"Error connecting to Telegram: {e}")
        
@app.route('/scan')
def scan_handler():
    # 1. Gather Data
    now = datetime.datetime.now().strftime("%I:%M %p | %b %d")
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    # Identify if it's iPhone or Android for a better icon
    device_icon = "📱"
    if "iPhone" in user_agent: device_icon = "🍏 iPhone"
    elif "Android" in user_agent: device_icon = "🤖 Android"

    # 2. Build a beautiful Telegram message
    msg = (
        f"<b>🔔 {BOT_NAME} Alert!</b>\n"
        f"━━━━━━━━━━━━━━━\n"
        f"📍 <b>Status:</b> Tag Scanned\n"
        f"⏰ <b>Time:</b> {now}\n"
        f"📱 <b>Device:</b> {device_icon}\n"
        f"━━━━━━━━━━━━━━━"
    )

    send_telegram_msg(msg)

    # 3. What the person who scanned sees (A clean landing page)
    return f"""
    <html>
        <head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
        <body style="text-align:center; font-family:sans-serif; background:#f4f4f9; padding-top:100px;">
            <div style="display:inline-block; background:white; padding:40px; border-radius:15px; shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h1 style="color:#0088cc; margin:0;">✔ Verified</h1>
                <p style="color:#666;">Scan recorded by {BOT_NAME}.</p>
            </div>
        </body>
    </html>
    """

if __name__ == '__main__':
    # Test message to let you know the server started
    print(f"Starting {BOT_NAME}...")
    app.run(host='0.0.0.0', port=5000)