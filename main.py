import telebot
import mysql.connector

bot = telebot.TeleBot('')

db = mysql.connector.connect(
    host="Andreybandit.mysql.pythonanywhere-services.com",
    user="Andreybandit",
    passwd="Tokoprovod",
    port="3306",
    database="Andreybandit$Tokoprovod"
    )

cursor = db.cursor()


sql = "SELECT size FROM details WHERE drawing = %s"
val = ("8ТП.310.017", )
cursor.execute(sql,val)

size = cursor.fetchall()
print(size)

# показат существующие базы данных
# cursor.execute("SHOW DATABASES")
#
# for x in cursor:
#     print(x)

# cursor.execute("CREATE TABLE details(drawing VARCHAR(50) UNIQUE, size VARCHAR(50), note VARCHAR(255))")

# cursor.execute("INSERT INTO details(drawing, size, note) values('test','plazma','test')")

# cursor.execute("SELECT * FROM details")

# cursor.execute("DROP TABLE details")

# print(mn)
# cursor.execute("SHOW TABLES")

# for x in cursor:
#     print(x)

# sql = "INSERT INTO details(drawing, size, note) VALUES(%s, %s, %s)"
# val = [
#     ]
# cursor.executemany(sql, val)
# db.commit()

# print(cursor.rowcount, "Запись добавлена")



# user_data = {}

# class User:
#     def __init__(self,firt_name):
#         self.firt_name = firt_name
#         self.last_name = ''

# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
#     msg = bot.send_message(message.chat.id,"Введите имя")
#     bot.register_next_step_handler(msg, process_firstname_step)

# def process_firstname_step(message):
#     try:
#         user_id = message.from_user.id
#         user_data[user_id] = User(message.text)

#         msg = bot.send_message(message.chat.id,"Введите фамилию")
#         bot.register_next_step_handler(msg, process_lastname_step)
#     except Exception as e:
#         bot.reply_to(message, 'oooops')

# def process_lastname_step(message):
#     try:
#         user_id = message.from_user.id
#         user = user_data[user_id]
#         user.last_name = message.text

#         bot.send_message(message.chat.id,"Вы успешно зарегестрированны")
#     except Exception as e:
#         bot.reply_to(message, 'oooops')

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
# bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
# bot.load_next_step_handlers()


bot.polling(none_stop=True)