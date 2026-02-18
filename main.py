import os
import logging
import asyncio
import threading
import re
import requests
from flask import Flask
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ==========================================
# 🔧 DEBUG LOGGING (បើកភ្នែកមើល Error)
# ==========================================
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

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
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@app.route('/')
def home():
    return "🤖 Spy Bot System is Active!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

@client.on(events.NewMessage(chats=SOURCE_CHAT_ID))
async def payment_handler(event):
    text = event.message.message
    # Print គ្រប់សារដែលចូលក្នុង Group (ដើម្បីតេស្ត)
    print(f"📩 ទទួលសារបាន៖ {text}") 

    if "paid by" in text and "$" in text:
        match = re.search(r"\$([\d.]+)", text)
        if match:
            amount = match.group(1)
            print(f"💰 ចាប់បានលុយ៖ ${amount} -> កំពុងផ្ញើទៅ PythonAnywhere...")
            try:
                payload = {'amount': amount, 'secret': SECRET_KEY}
                r = requests.post(WEB_URL, json=payload, timeout=10)
                print(f"✅ Server ឆ្លើយតប៖ {r.status_code} - {r.text}")
            except Exception as e:
                print(f"❌ បរាជ័យ៖ {e}")

async def start_telethon():
    print("🚀 កំពុងព្យាយាមភ្ជាប់ទៅ Telegram...")
    await client.start()
    
    # 🔥 តេស្តផ្ញើសារចូល Saved Messages ខ្លួនឯង
    try:
        me = await client.get_me()
        print(f"✅ ជោគជ័យ! បាន Login ក្នុងឈ្មោះ: {me.first_name}")
        await client.send_message('me', f"🤖 **Spy Bot ដំណើរការហើយនៅលើ Render!**\n📅 {os.environ.get('RENDER_INSTANCE_ID', 'Local')}")
        print("📨 បានផ្ញើសារតេស្តទៅកាន់ 'Saved Messages' ហើយ!")
    except Exception as e:
        print(f"⚠️ មិនអាចផ្ញើសារតេស្តបាន៖ {e}")

    print(f"🎧 កំពុងចាំស្តាប់សារពី Channel ID: {SOURCE_CHAT_ID}")
    await client.run_until_disconnected()

def run_bot_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_telethon())

if __name__ == "__main__":
    # បំបែក Thread ឱ្យ Flask និង Telethon ដើរទន្ទឹមគ្នា
    t = threading.Thread(target=run_bot_loop)
    t.start()
    run_flask()
