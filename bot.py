import telebot
import time
from main import parser
from main import Search

token = "8512618246:AAEjTE811MNq1xbWwmg7VOmCJfzOfn8glzM"
bot = telebot.TeleBot(token)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет! Что бы проверить определенные заказы на ВБ пропишите комманду (/pars 'То что именно вы хотите запарсить')")
@bot.message_handler(commands=["pars"])
def pars(message):
    command_text = message.text
    parts = command_text.split(maxsplit=1)
    if len(parts) > 1:
        search_query = parts[1]  #отправляет сам запрос в парсер меняя под запрос url
        
        bot.send_message(message.chat.id, f"🔍 Начинаю парсинг по запросу: '{search_query}'...")
        
        # Передаём запрос в парсер
        url = Search(search_query)

        all_product = parser(url)
        for _ in all_product:
            bot.send_message(
            message.chat.id,
            f'Название: {_["title"]}\n Цена: {_["price"]}\n Ссылка: {_["link"]}\nПриедет: {_["data"]}\nОценка: {_["rate"]}\nБренд: {_["brand"]}'
        ) #отправляет данные через комманду
        time.sleep(0.1) #задержка что бы не произошло ошибки
print("Работает")
bot.polling()