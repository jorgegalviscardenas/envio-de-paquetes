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
@param Base modelo El modelo sobre el cual se hacen las actualizaciones
@param Dict datos Los datos que se actualizan del modelo en la base de datos
'''


def actualizar_datos_modelo(modelo, datos):
    for llave, valor in datos.items():
        setattr(modelo, llave, valor)
    db.session.commit()


'''
Encargado de generar el número de guía para el paquete. La generación es aleatoria
@return string cadena de 10 digitos
'''


def generar_numero_guia():
    letters = string.digits
    return ''.join(random.choice(letters) for i in range(10))


'''
Obtiene el cliente que se va a terminar de registrar
@param string id identificador del cliente
@return Cliente El cliente encontrado
'''


def obtener_cliente_registro(id):
    cliente = db.session.query(Cliente).get(id)
    return cliente


'''
Encargado de listar los paqueres con rol administrador
'''


def listar_paquetes():
    paquetes = db.session.query(Paquete).filter(
        Paquete.estado_actual == 1
    ).order_by(Paquete.creado_el.asc()).all()

    return paquetes

'''
Obtiene los paquetes de un determinado cliente
@param string id identificador del cliente
@return listado de paquetes del cliente
'''

def listar_mis_paquetes(id):
    paquetes = db.session.query(Paquete).filter(
        Paquete.cliente_id == id,
        Paquete.estado_actual_objeto!=None
    ).order_by(Paquete.estado_actual.asc()).order_by(Paquete.creado_el.asc()).all()
    return paquetes


'''
Obtiene el mensaje por defecto que se le muestra al usuario
cuando no se entendio lo que ingreso
@return string
'''


def get_fallback_message(text):
    response = f"\U0001F648 No entendí lo que me acabas de decir"
    return response
