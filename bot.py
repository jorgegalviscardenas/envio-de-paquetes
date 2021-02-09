#########################################################

from config import bot,config
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
@bot.message_handler(func=lambda message: True)
def on_fallback(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    response = logic.get_fallback_message(message.text)
    bot.reply_to(message, response)
#########################################################
if __name__ == '__main__':
    bot.polling(timeout=20)
#########################################################