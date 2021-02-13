'''
Encargado de toda la lógica de los diferentes comandos y/o mensajes
que va a procesar el bot.

@author Sebastian Noreña Marquez <sebastian.norenam@autonoma.edu.co>
@author Camilo Andres Lengua Duque <camiloa.lenguad@autonoma.eu.co>
@author Alejandro Gomez Alzate <alejandro.gomez@autonoma.edu.co>
@author Jorge Galvis Cárdenas <jorge.galvisc@autonoma.edu.co>

@version 20210209
'''
import database.db as db
from models.Evento import Evento
from models.Cliente import Cliente
from models.Estado import Estado
from models.Paquete import Paquete
from models.Usuario import Usuario
import telebot
import random
import string

'''
Construye el menú de acuerdo si es un usuario del sistema o un cliente
@param string id identificador del usuario
@return markup con las opciones que puede hacer en el bot
'''


def construir_menu(id):
    usuario = db.session.query(Usuario).get(id)
    db.session.commit()
    if usuario == None:
        cliente = db.session.query(Cliente).get(id)
        db.session.commit()
        if cliente != None:
            return cliente.construir_menu()
        else:
            return None
    else:
        return usuario.construir_menu()


'''
Encargado de crear el cliente. Solo se crea si no existe como usuario ni como cliente
@param string id identificador del usuario en Telegram
@param string nombres nombres del usuario en Telegram
@param string apellidos apellidos del usuario en Telegram
'''


def registrar_cliente(id, nombres, apellidos):
    usuario = db.session.query(Usuario).get(id)
    db.session.commit()
    if usuario == None:
        cliente = db.session.query(Cliente).get(id)
        db.session.commit()
        if cliente == None:
            cliente = Cliente(id, nombres, apellidos)
            db.session.add(cliente)
            db.session.commit()


'''
Encargado de construir las opciones para estado que se tiene
'''


def construir_opciones_estado():
    markup = telebot.types.InlineKeyboardMarkup()
    estados = db.session.query(Estado).all()
    for estado in estados:
        markup.add(telebot.types.InlineKeyboardButton(
            text=estado.nombre, callback_data=estado.id))
    return markup


'''
Obtiene el paquete que se va a registrar para un usuario especifico.
En caso de que haya un paquete pendiente toma ese, sino crea uno
@param string id identificador del cliente
@return Paquete el paquete que se encontró o se creo
'''


def obtener_paquete_creacion(id):
    paquete = db.session.query(Paquete).filter_by(
        cliente_id=id
    ).filter_by(
        estado_actual=None
    ).first()
    db.session.commit()
    if not paquete:
        paquete = Paquete(id)
        db.session.add(paquete)
        db.session.commit()
    return paquete


'''
Actualiza datos de un paquete
@param Paquete paquete El paquete sobre el cual se hacen las actualizaciones
@param Dict datos Los datos que se actualizan en el paquete
'''


def actualizar_datos_paquete(paquete, datos):
    for llave, valor in datos.items():
        setattr(paquete, llave, valor)
    db.session.commit()


'''
Encargado de generar el número de guía para el paquete. La generación es aleatoria
@return string cadena de 10 digitos
'''


def generar_numero_guia():
    letters = string.digits
    return ''.join(random.choice(letters) for i in range(10))


'''
Obtiene el mensaje por defecto que se le muestra al usuario
cuando no se entendio lo que ingreso
@return string
'''


def get_fallback_message(text):
    response = f"\U0001F648 No entendí lo que me acabas de decir"
    return response
