import telebot
import mysql.connector


bot = telebot.TeleBot('5796781509:AAH6nFu_T5zdRV7DEFg4BzkTHyktZ7N30Bw')

mydb = mysql.connector.connect(
    host="Andreybandit.mysql.pythonanywhere-services.com",
    user="Andreybandit",
    passwd="Tokoprovod",
    port="3306"
    )

print(mydb)

user_data = {}

class User:
    def __init__(self,firt_name):
        self.firt_name = firt_name
        self.last_name = ''

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    msg = bot.send_message(message.chat.id,"Введите имя")
    bot.register_next_step_handler(msg, process_firstname_step)

def process_firstname_step(message):
    try:
        user_id = message.from_user.id
        user_data[user_id] = User(message.text)

        msg = bot.send_message(message.chat.id,"Введите фамилию")
        bot.register_next_step_handler(msg, process_lastname_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_lastname_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.last_name = message.text

        bot.send_message(message.chat.id,"Вы успешно зарегестрированны")
    except Exception as e:
        bot.reply_to(message, 'oooops')

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.polling(none_stop=True)



if __name__**'__main__': # Убрать для PythonAnyWhere
    bot.polling(none_stop=True)