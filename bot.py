#########################################################

from config import bot
import config
from time import sleep
import re
import logic
import database.db as db
#########################################################
# Aquí vendrá la implementación de la lógica del bot
#########################################################

if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
#########################################################

@bot.message_handler(commands=['start'])
def on_command_start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    
    bot.send_message(
        message.chat.id,
        logic.get_welcome_message(bot.get_me()),
        parse_mode="Markdown")

########################################################
#Temporal, función para listar los pedidos de un administrador

@bot.message_handler(commands=['listar'])
def on_list_packages(message):
    bot.send_chat_action(message.chat.id, 'typing')
    
    usuarios = logic.listar_usuarios()

    text = ""
    
    for e in usuarios:
            text += f"| {e.id} | ${e.nombre} ) |\n"

    bot.reply_to(message, text, parse_mode="Markdown")

########################################################

@bot.message_handler(func=lambda message: True)
def on_fallback(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    response = logic.get_fallback_message(message.text)
    bot.reply_to(message, response)
#########################################################
if __name__ == '__main__':
    # db.Base.metadata.create_all(db.engine)
    bot.polling(timeout=20)
#########################################################