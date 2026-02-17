import os
import asyncio
import threading
import re
import requests
from flask import Flask
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ==========================================
# ⚙️ CONFIGURATION
# ==========================================
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
SOURCE_CHAT_ID = int(os.environ.get("SOURCE_CHAT_ID"))
WEB_URL = os.environ.get("WEB_URL")
SECRET_KEY = os.environ.get("SECRET_KEY")

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Spy Bot is Running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ==========================================
# 🕵️ SPY BOT LOGIC
# ==========================================
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH, loop=loop)

@client.on(events.NewMessage(chats=SOURCE_CHAT_ID))
async def payment_handler(event):
    # 🔥 បើកកន្លែងនេះវិញ ដើម្បីមើលសារដែលចូល
    text = event.message.message
    print(f"📩 សារចូលថ្មី: {text}") 

    if "paid by" in text and "$" in text:
        match = re.search(r"\$([\d.]+)", text)
        if match:
            amount = match.group(1)
            print(f"💰 ចាប់បានលុយ: ${amount} | កំពុងផ្ញើទៅ Bot...")
            try:
                payload = {'amount': amount, 'secret': SECRET_KEY}
                # បន្ថែម verify=False ក្រែងលោមានបញ្ហា SSL
                r = requests.post(WEB_URL, json=payload, timeout=10)
                print(f"✅ Bot ឆ្លើយតប: {r.status_code} - {r.text}")
            except Exception as e:
                print(f"❌ បរាជ័យក្នុងការផ្ញើ: {e}")

def run_telethon():
    print(f"🚀 កំពុងភ្ជាប់ទៅ Telegram... (ស្តាប់ ID: {SOURCE_CHAT_ID})")
    try:
        client.start()
        print("✅ បានភ្ជាប់ទៅ Telegram ជោគជ័យ!")
        client.run_until_disconnected()
    except Exception as e:
        print(f"🔥 Error Telethon: {e}")

if __name__ == "__main__":
    t = threading.Thread(target=run_telethon)
    t.start()
    run_flask()
