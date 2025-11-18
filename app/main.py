import os
import signal
import time
from dotenv import load_dotenv
import telebot
import threading
import logging

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
if not TELEGRAM_TOKEN:
    raise RuntimeError('TELEGRAM_TOKEN is not set in environment')

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger('invebot-worker')

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode='HTML')

# --- Example handlers ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет! Бот запущен (Render Worker). Я не даю финансовых советов.')


# Add more handlers or import them from your handlers/ package
# from handlers.start import register_handlers
# register_handlers(bot)

# Polling thread
polling_thread = None
stop_flag = False

def polling_loop():
    logger.info('Starting bot.polling (long polling)')
    while not stop_flag:
        try:
            bot.polling(none_stop=True, interval=2, timeout=20)
        except Exception as e:
            logger.exception('Exception in polling: %s', e)
            time.sleep(5)
    logger.info('Exiting polling loop')

def start_polling_in_thread():
    global polling_thread
    polling_thread = threading.Thread(target=polling_loop, name='PollingThread', daemon=True)
    polling_thread.start()

def stop_polling():
    global stop_flag
    stop_flag = True
    try:
        bot.stop_polling()
    except Exception:
        pass
    if polling_thread and polling_thread.is_alive():
        polling_thread.join(timeout=5)

def handle_signal(signum, frame):
    logger.info('Received signal %s, stopping...', signum)
    stop_polling()

if __name__ == '__main__':
    # Hook termination signals for graceful shutdown
    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)
    logger.info('InveBot worker starting...')
    start_polling_in_thread()
    # Keep the main thread alive while polling runs in background
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info('KeyboardInterrupt received, stopping...')
        stop_polling()
