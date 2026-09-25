import time
import os
import telebot
import google.genai as genai

# قراءة التوكنات من متغيرات البيئة (بدل ما تكون مكتوبة في الكود)
TELEGRAM_TOKEN = "8904114683:AAENUy809C8G6DwP6voN5dGjlBbeL-ceuQ4"
GEMINI_API_KEY = "AIzaSyD-GD61c2qUVracTj_T_2yhxYuXM4tsPgQ"

# التحقق من وجود التوكنات
if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    raise ValueError("❌ التوكنات غير موجودة! تأكد من ضبط متغيرات البيئة TELEGRAM_TOKEN و GEMINI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

# محاولة حذف أي webhook سابق لتجنب خطأ 409
try:
    bot.remove_webhook()
    time.sleep(1)
except Exception as e:
    print(f"Webhook removal note: {e}")

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message,
        "Welcome to the Continental.\nI am John Wick... Powered by AI.\nHow can I help you today?"
    )

@bot.message_handler(func=lambda message: True)
def ai_reply(message):
    try:
        bot.send_chat_action(message.chat.id, "typing")
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=message.text,
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(
            message,
            "⚠️ حدث خطأ أثناء الاتصال بالذكاء الاصطناعي، يرجى المحاولة مجدداً."
        )
        print(f"Error details: {e}")

if __name__ == "__main__":
    print("🤖 Bot is running...")
    bot.infinity_polling()
