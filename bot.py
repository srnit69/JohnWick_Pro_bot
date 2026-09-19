import time
import google.genai as genai
import telebot

TELEGRAM_TOKEN = "8904114683:AAEMNJzjx38G7IANviA9NsRYrt9pc42xBhA"

# ضعي مفتاح AI Studio الحقيقي الذي يبدأ بـ AIzaSy
GEMINI_API_KEY = "AIzaSyD-GD61c2qUVracTj_T_2yhxYuXM4tsPgQ"

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
        "Welcome to the Continental. I am John Wick... Powered by AI. How can I help you today?",
    )


@bot.message_handler(func=lambda message: True)
def ai_reply(message):
    try:
        bot.send_chat_action(message.chat.id, "typing")

        # تم تصحيح اسم الموديل إلى gemini-1.5-flash
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=message.text,
        )

        bot.reply_to(message, response.text)

    except Exception as e:
        bot.reply_to(
            message,
            "حدث خطأ أثناء الاتصال بالذكاء الاصطناعي، يرجى المحاولة مجدداً.",
        )
        print(f"Error details: {e}")


bot.infinity_polling()