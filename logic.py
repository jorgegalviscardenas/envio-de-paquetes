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
from sqlalchemy import desc
from models.Evento import Evento
from models.Cliente import Cliente
from models.Estado import Estado
from models.Paquete import Paquete
from models.Usuario import Usuario
from datetime import datetime
import telebot
import random
import string

ID_ENTREGADO = 6

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
        Paquete.estado_actual != 6
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

'''
Generar un evento para un paquete que aún no se encuentra entregado
@param usua_id integer
@param nguia string
return string
'''
def evento_paquete_guia (usua_id, nguia):
    paquete = get_paquete_numero_guia(nguia)
    if not paquete:
        return f"\U0000274C No existe un paquete para el número de guía indicado."
    if paquete.estado_actual == ID_ENTREGADO:
        return f"\U0000274C Este paquete ya se encuentra entregado y no se le pueden agregar más eventos."

    evento = get_evento_id_creado_por_paquete_id(usua_id, paquete.id)
    #valida si un evento ya existe para no crear varios eventos incompletos
    if not evento:    
        evento = Evento(
            None,
            datetime.now(),
            None,
            usua_id,
            paquete.id)

        db.session.add(evento)
        
        db.session.commit()
     
    else:
        evento.creado_el = datetime.now()

        db.session.commit()

    return "OK"

'''
Actualizar un evento de un usuario para asignarle un estado
@param usua_id integer
@param estado_id integer
return boolean
'''
def update_evento_estado_id (usua_id, estado_id):
    evento = get_evento_creado_por(usua_id)
    if not evento:
        return f"\U0000274C No se encuentra un evento para el usuario, intente iniciar de nuevo."

    paquete = evento.paquete

    if estado_id == paquete.estado_actual:
        return f"\U0000274C El paquete ya se encuentra en este estado, se debe cambiar a un estado diferente."

    evento.estado_id = estado_id
    
    db.session.commit()

    return "OK"

'''
Actualizar un evento de un usuario para asignarle la fecha
@param usua_id integer
@param arrFecha Array<string>
return boolean
'''
def update_evento_fecha (usua_id, arrFecha):
    evento = get_evento_creado_por(usua_id)
    if not evento:
        return f"\U0000274C Error, asegúrese de estar cambiando el estado de un solo paquete y vuelva a intentarlo."

    paquete = evento.paquete
    try:
        evento.fecha = datetime(int(arrFecha[1]),int(arrFecha[2]),int(arrFecha[3]),int(arrFecha[4]),int(arrFecha[5]),0)
    except:
        return f"\U0000274C Error, asegúrese de estar ingresando la fecha en el formato (yyyy-MM-dd HH:mm)\U0000274C"

    paquete.estado_actual = evento.estado_id
    paquete.fecha_estado_actual = datetime.now()
    evento.creado_el = datetime.now()

    db.session.commit()

    return "OK"

'''
Obtener un paquete por número de guia
@param numero_guia string 
@return Paquete
'''
def get_paquete_numero_guia (nguia):
    paquete = db.session.query(Paquete
        ).filter_by(numero_guia=nguia
        ).first()
    
    db.session.commit()

    return paquete

'''
Obtener un paquete por id
@param paquete_id integer 
@return Paquete
'''
def get_paquete_id (paquete_id):
    paquete = db.session.query(Paquete
        ).filter_by(id=paquete_id
        ).first()
    
    db.session.commit()

    return paquete

'''
Obtener un evento por creado_por y que el campo 
creado_el se encuentre vacio
@param usua_id integer
return Evento
'''
def get_evento_creado_por(usua_id):
    evento = db.session.query(Evento
        ).filter_by(creado_por=usua_id
        ).filter_by(fecha=None
        ).order_by(desc(Evento.creado_el)
        ).first()

    db.session.commit()
    
    return evento

'''
Obtener un evento por id, paquete_id y creado_por
para identificar el evento que se está editando
@param evento_id integer
@param usua_id integer
@param paquete_id integer
return Evento
'''
def get_evento_id_creado_por_paquete_id(usua_id, paquete_id):
    evento = db.session.query(Evento
        ).filter_by(creado_por=usua_id
        ).filter_by(paquete_id=paquete_id
        ).filter_by(fecha=None
        ).filter_by(estado_id=None
        ).order_by(desc(Evento.creado_el)
        ).first()

    db.session.commit()
    
    return evento
