import os
import asyncio
import threading
import re
import requests
from flask import Flask
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ==========================================
# ⚙️ CONFIGURATION (យកពី Render Setting)
# ==========================================
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

# Payment Group & Webhook
SOURCE_CHAT_ID = int(os.environ.get("SOURCE_CHAT_ID", "-1003814961700"))
WEB_URL = os.environ.get("WEB_URL", "https://Godss.pythonanywhere.com/api/confirm_payment")
SECRET_KEY = os.environ.get("SECRET_KEY", "Lava12345_Auto_Secret")

# ==========================================
# 🌐 WEB SERVER (FLASK) - ដើម្បីឱ្យ Render ស្គាល់ថាជា Web Service
# ==========================================
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Spy Bot is Running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ==========================================
# 🕵️ SPY BOT LOGIC (TELETHON)
# ==========================================
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH, loop=loop)

@client.on(events.NewMessage(chats=SOURCE_CHAT_ID))
async def payment_handler(event):
    text = event.message.message
    print(f"📩 New MSG: {text}")

    if "paid by" in text and "$" in text:
        match = re.search(r"\$([\d.]+)", text)
        if match:
            amount = match.group(1)
            print(f"💰 Found: ${amount}")
            try:
                payload = {'amount': amount, 'secret': SECRET_KEY}
                requests.post(WEB_URL, json=payload, timeout=10)
                print("✅ Sent to Main Bot")
            except Exception as e:
                print(f"❌ Error sending: {e}")

def run_telethon():
    print("🚀 Starting Telethon Client...")
    client.start()
    client.run_until_disconnected()

# ==========================================
# 🚀 MAIN ENTRY POINT
# ==========================================
if __name__ == "__main__":
    t = threading.Thread(target=run_telethon)
    t.start()
    run_flask()