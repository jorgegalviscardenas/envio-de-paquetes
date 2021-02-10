from models.Evento import Evento
from models.Cliente import Cliente
from models.Estado import Estado
from models.Paquete import Paquete
from models.Usuario import Usuario

###########################################################

def get_welcome_message(bot_data):
    response = (
        f"Hola, soy *{bot_data.first_name}* "
        f"también conocido como *{bot_data.username}*.\n\n"
        "¡Estoy aquí para ayudarte a administrar la información de tus paquetes!"
    )
    return response

###########################################################

def get_fallback_message (text):
    response = f"\U0001F648 No entendí lo que me acabas de decir"
    return response