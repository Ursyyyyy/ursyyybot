import telebot
import const
import botcommands
from telebot import types

bot = telebot.TeleBot(const.token)

flag = False

#Вывод информации по командам для обычных пользователей
@bot.message_handler(commands= ['help'])
def react(message):
        bot.reply_to(message, """/login - login, but u can do it, if know necessary info""")
        log(message)

#Реализация автоцации
@bot.message_handler(commands= ['login'])
def login(message):
        if(flag):
                bot.send_message(message.from_user.id, "You have been logined already")
        else:
                bot.send_message(message.chat.id, "Please login")
                bot.send_message(message.from_user.id, "Input a admin name:")
                bot.register_next_step_handler(message, adm_name)
        log(message)
def adm_name(message):
        if message.text == botcommands.aname:
                bot.send_message(message.from_user.id, "Input a admin password:")
                bot.register_next_step_handler(message, adm_pass)
        else:
                bot.send_message(message.chat.id, "Wrong username!")
        log(message)
def adm_pass(message):
        if message.text == botcommands.apass:
                bot.send_message(message.from_user.id, "Tipe /ahelp for take info")
                global flag
                flag = True
                return flag
        else:
                bot.send_message(message.from_user.id, "Wrong password!")
        log(message)

#Деавторизация пользователя
@bot.message_handler(commands= ['logout'])
def loguot(message):
        global flag
        flag = False

#Вывод помощи по командам для админа
@bot.message_handler(commands = ['ahelp'])
def adminhelp(message):
        if message.text == '/ahelp' and flag == True:
                bot.send_message(message.from_user.id, botcommands.adminhelp)
#Смена пароля или имени админа
@bot.message_handler(commands = ['chadmname', 'chadmpass'])
def change(message):
        if message.text == '/chadmname' and flag == True:
                bot.send_message(message.from_user.id, "Input new admin username:")
                bot.register_next_step_handler(message, chpname)
        if message.text == '/chadmpass' and flag == True:
                bot.send_message(message.from_user.id, "Input new admin password:")
                bot.register_next_step_handler(message, chpass)
def chpname(message): 
        botcommands.aname = str(message.text)
        bot.send_message(message.from_user.id, botcommands.chaname + message.text)
def chpass(message):
        botcommands.apass = str(message.text)  
        bot.send_message(message.from_user.id, botcommands.chapass + message.text)

#Вывод нформации о поступленом сообщени на консоль
def log(message):
    print("\n ------")
    from datetime import datetime
    print(datetime.now())
    print("Сообщение от {0}. (id = {1}) \nТекст = {2}".format(message.from_user.first_name,
                                                        str(message.from_user.id), message.text))

#Зацикливание бота(бот работает постоянно)
bot.polling(none_stop=True)
