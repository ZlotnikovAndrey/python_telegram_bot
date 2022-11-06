import telebot

token = '5796781509:AAH6nFu_T5zdRV7DEFg4BzkTHyktZ7N30Bw'

bot = telebot.TeleBot(token)

@bot.message_handler(content_types=["text"])
def echo(message):
    bot.send_message(message.chat.id, message.text)


bot.polling(none_stop=True)