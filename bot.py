import time
import google.genai as genai
import telebot
import os

# قراءة التوكنات من متغيرات البيئة (Secrets في GitHub Actions)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# التحقق من وجود التوكنات
if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    raise ValueError("❌ التوكنات غير موجودة! تأكد من وضعها داخل Secrets في GitHub.")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

# تفريغ أي جلسة سابقة لتجنب خطأ 409
try:
    bot.remove_webhook()
    time.sleep(1)
except Exception:
    pass


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


bot.infinity_polling()
