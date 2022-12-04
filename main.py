import telebot
import mysql.connector
from telebot import types # для указание типов

bot = telebot.TeleBot('')

name = '';                 # переменная для поиска развертки по чертежу детали
shell_thickness = 0;       # переменная для поиска развертки обечайки
shell_diameter = 0;        # переменная для поиска развертки обечайки
half_shell_thickness = 0;  # переменная для поиска развертки полуоболочки
half_shell_diameter = 0;   # переменная для поиска развертки полуоболочки
straight_part = 0;         # переменная для поиска развертки полуоболочки

@bot.message_handler(commands=['start']) # стартовая функция с тремя кнопками функций бота
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton("Развертку обечайки")
    btn2 = types.KeyboardButton("Развертку полуоболочки")
    btn3 = types.KeyboardButton("Развертку детали по чертежу")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "Привет, Я  бот ЦТК, могу помочь рассчитать развертку обечайки или подсказать развертку детали. Выберете что вам нужно ", reply_markup=markup)

@bot.message_handler(content_types=['text']) # перенаправление на функции, после нажатия определенной кнопки. И получение начальных данных
def func(message):
    if(message.text == "Развертку детали по чертежу"):
        name = bot.send_message(message.chat.id,"Введите чертеж детали")
        bot.register_next_step_handler(name, get_drawing)
    elif(message.text == "Развертку обечайки"):
        shell_diameter = bot.send_message(message.chat.id,"Введите <b>ВНЕШНИЙ</b> диаметр",parse_mode='html')
        bot.register_next_step_handler(shell_diameter, get_thickness)
    elif(message.text == "Развертку полуоболочки"):
        half_shell_diameter = bot.send_message(message.chat.id,"Введите <b>ВНУТРЕННИЙ</b> диаметр",parse_mode='html')
        bot.register_next_step_handler(half_shell_diameter, get_half_thickness)

def get_drawing(message): #функция нахождения данных в базе данных MySQL
    try:
        global name;
        name = message.text;

        db = mysql.connector.connect(
            host="Andreybandit.mysql.pythonanywhere-services.com",
            user="Andreybandit",
            passwd="Tokoprovod",
            port="3306",
            database="Andreybandit$Tokoprovod"
            )
        cursor = db.cursor()

        sql = "SELECT size FROM details WHERE drawing = %s"
        val = (name, )
        cursor.execute(sql,val)
        size = cursor.fetchall()
        cursor.close()
        bot.send_message(message.from_user.id, size);
    except Exception:
        bot.send_message(message.from_user.id, '<b>Данная деталь не найдена</b>, убедитесь что чертеж детали указан верно, пример <b> 8ТП.000.001-001</b>', parse_mode='html');

def get_thickness(message):            # запрос у пользователя данных о толщине стенки оболочки 
    global shell_diameter;
    shell_diameter = message.text
    shell_thickness = bot.send_message(message.chat.id,"Введите толщину стенки")
    bot.register_next_step_handler(shell_thickness, scope_shell)

def scope_shell(message):             # расчет развертки обечайки. Вывод результата или ошибки
    try:
        shell_thickness = message.text
        scope_size = ( float(shell_diameter) - float(shell_thickness) ) * 3.14
        bot.send_message(message.from_user.id,scope_size);
    except Exception:
        bot.send_message(message.from_user.id, '<b>убедитесь что вводили цифры</b>', parse_mode='html');

def get_half_thickness(message): # запрос у пользователя данных о толщине стенки полуоболочки 
    global half_shell_diameter;
    half_shell_diameter = message.text
    half_shell_thickness = bot.send_message(message.chat.id,"Введите толщину стенки")
    bot.register_next_step_handler(half_shell_thickness, get_straight_part)

def get_straight_part(message):        # запрос у пользователя данных прямого участка полуоболочки 
    global half_shell_thickness;
    half_shell_thickness = message.text
    straight_part = bot.send_message(message.chat.id,"Введите длину прямого участка")
    bot.register_next_step_handler(straight_part, scope_half_shell)

def scope_half_shell(message):  # расчет развертки полуоболочки. Вывод результата или ошибки
    try:
        global straight_part;
        straight_part = message.text
        scope_half_shell = (((int(half_shell_diameter) + int(half_shell_thickness)) * 3.14) / 2) + (int(straight_part) * 2)
        bot.send_message(message.from_user.id, scope_half_shell);
    except Exception:
        bot.send_message(message.from_user.id, '<b>убедитесь что вводили цифры</b>', parse_mode='html');


bot.polling(none_stop=True)