import telebot
import logging
import locale
import time
from datetime import datetime,timedelta
from decouple import config

#########################################################
try:
    locale.setlocale(locale.LC_TIME, "es_CO.utf8") 
except:
    print("No pude configurar localización")
# Versión del bot

VERSION = 0.1

# Obtiene el token desde el archivo de configuración
TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')

#########################################################

# Crea el objeto bot utilizando el token
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Determina el nivel de los mensajes que se van a mostrar (debug)
telebot.logger.setLevel(logging.INFO)

#########################################################