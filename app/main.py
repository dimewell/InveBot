import os
import telebot
from fastapi import FastAPI
from dotenv import load_dotenv
import threading
from openai import OpenAI

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(api_key=OPENAI_KEY)

app = FastAPI()

@app.get("/")
def home():
    return {"status": "bot is running"}

def ask_gpt(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Ошибка OpenAI: {e}"

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Отправь сообщение — я отвечу через OpenAI.")

@bot.message_handler(func=lambda m: True)
def reply(message):
    answer = ask_gpt(message.text)
    bot.send_message(message.chat.id, answer)

def run_bot():
    bot.infinity_polling(skip_pending=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
