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
# 🔧 DEBUG LOGGING
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

# ✅ ID ឆានែលថ្មីសម្រាប់ទទួលលុយ (កន្លែងដែលត្រូវផ្ញើចូល)
TARGET_CHANNEL_ID = -1003884565688

app = Flask(__name__)
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@app.route('/')
def home():
    return "🤖 Spy Bot System is Active!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ==========================================
# 📩 PAYMENT HANDLER
# ==========================================
# នៅស្តាប់តែ Source ដើមដដែល
@client.on(events.NewMessage(chats=SOURCE_CHAT_ID))
async def payment_handler(event):
    text = event.message.message
    # Print គ្រប់សារដែលចូលក្នុង Group (ដើម្បីតេស្ត)
    print(f"📩 ទទួលសារបាន៖ {text}") 

    if "paid by" in text and "$" in text:
        match = re.search(r"\$([\d.]+)", text)
        if match:
            amount = match.group(1)
            print(f"💰 ចាប់បានលុយ៖ ${amount}")

            # 1️⃣ ផ្នែកទី ១៖ ផ្ញើទៅ PythonAnywhere (មុខងារដើម)
            try:
                print(" -> កំពុងផ្ញើទៅ PythonAnywhere...")
                payload = {'amount': amount, 'secret': SECRET_KEY}
                r = requests.post(WEB_URL, json=payload, timeout=10)
                print(f"✅ Server ឆ្លើយតប៖ {r.status_code} - {r.text}")
            except Exception as e:
                print(f"❌ Server បរាជ័យ៖ {e}")

            # 2️⃣ ផ្នែកទី ២៖ ផ្ញើចូល Channel ថ្មីភ្លាមៗ (មុខងារបន្ថែមថ្មី)
            try:
                print(f" -> កំពុង Forward ទៅ Channel {TARGET_CHANNEL_ID}...")
                
                # បង្កើតសារជូនដំណឹង
                alert_message = (
                    f"🔔 **ចាប់បានការបាញ់លុយថ្មី!**\n"
                    f"💰 ចំនួន: **${amount}**\n"
                    f"➖➖➖➖➖➖➖\n"
                    f"{text}"
                )
                
                # ផ្ញើសារចូល Channel ថ្មី
                await client.send_message(TARGET_CHANNEL_ID, alert_message)
                print("✅ បានផ្ញើចូល Channel ថ្មីជោគជ័យ!")
            except Exception as e:
                print(f"❌ ផ្ញើចូល Channel ថ្មីបរាជ័យ៖ {e}")

async def start_telethon():
    print("🚀 កំពុងព្យាយាមភ្ជាប់ទៅ Telegram...")
    await client.start()
    
    # 🔥 តេស្តផ្ញើសារចូល Saved Messages ខ្លួនឯង
    try:
        me = await client.get_me()
        print(f"✅ ជោគជ័យ! បាន Login ក្នុងឈ្មោះ: {me.first_name}")
        await client.send_message('me', f"🤖 **Spy Bot ដំណើរការហើយនៅលើ Render!**\n📅 {os.environ.get('RENDER_INSTANCE_ID', 'Local')}")
    except Exception as e:
        print(f"⚠️ មិនអាចផ្ញើសារតេស្តបាន៖ {e}")

    print(f"🎧 កំពុងចាំស្តាប់សារពី Channel ID: {SOURCE_CHAT_ID}")
    await client.run_until_disconnected()

def run_bot_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_telethon())

if __name__ == "__main__":
    t = threading.Thread(target=run_bot_loop)
    t.start()
    run_flask()
