import telebot
import requests
import re

TOKEN = "8878883328:AHAh3sD-Cf3b9M0PAihbvVqpw9TEURCAx6Q"  # Ganti nanti kalau direset

bot = telebot.TeleBot(TOKEN)

def bypass_redirect(url):
    try:
        session = requests.Session()
        resp = session.get(url, allow_redirects=True, timeout=30)
        return resp.url
    except Exception as e:
        return f"Error: {str(e)}"

def bypass_advanced(url):
    try:
        api_url = f"https://api.bypass.vip/?url={url}"
        resp = requests.get(api_url, timeout=20)
        data = resp.json()
        if data.get("success"):
            return data.get("destination")
        return f"Gagal: {data.get('message', 'unknown')}"
    except Exception as e:
        return f"Error API: {str(e)}"

def is_advanced_shortener(url):
    domains = ['ouo.io', 'linkvertise', 'adf.ly', 'shorte.st', 'exe.io']
    return any(d in url for d in domains)

@bot.message_handler(commands=['start', 'help'])
def help_cmd(message):
    bot.reply_to(message, "🤖 Kirim link pendek, aku kasih link asli.")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    urls = re.findall(r'https?://[^\s]+', message.text)
    if not urls:
        bot.reply_to(message, "Kirim link yang mau dibypass.")
        return
    link = urls[0]
    bot.reply_to(message, f"⏳ Memproses...")
    result = bypass_advanced(link) if is_advanced_shortener(link) else bypass_redirect(link)
    bot.reply_to(message, f"🔓 {result}")

if __name__ == "__main__":
    print("✅ Bot berjalan!")
    bot.infinity_polling()
