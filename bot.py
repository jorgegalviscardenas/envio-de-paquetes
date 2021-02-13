#########################################################

from config import bot
import config
from time import sleep
import re
import logic
import database.db as db
import telebot
from models.Estado import Estado
from datetime import datetime
import validadores
#########################################################
# Aquí vendrá la implementación de la lógica del bot
#########################################################

if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
#########################################################

'''
Encargado de iniciar el bot. En esta función se hace el registro del cliente.
Se hace a través del comando
'''


@bot.message_handler(commands=['start'])
def comando_start(mensaje):
    bot.send_chat_action(mensaje.chat.id, 'typing')
    logic.registrar_cliente(
        mensaje.from_user.id, mensaje.from_user.first_name, mensaje.from_user.last_name)
    markup = logic.construir_menu(mensaje.from_user.id)
    bot.send_message(
        mensaje.chat.id, text="Estas son las opciones que te puedo ofrecer", reply_markup=markup)


'''
Encargado de mostrar el menú con las opciones.
Se puede hacer a través del comando /menu /help
'''


@bot.message_handler(commands=['menu', 'help'])
def comando_menu(mensaje):
    bot.send_chat_action(mensaje.chat.id, 'typing')
    logic.generar_numero_guia()
    markup = logic.construir_menu(mensaje.from_user.id)
    if(markup != None):
        bot.send_message(
            mensaje.chat.id, text="Estas son las opciones que te puedo ofrecer", reply_markup=markup)
    else:
        bot.send_message(
            mensaje.chat.id, text="Por favor ejecuta el comando /start para iniciar el bot")


'''
Encargado de recibir la petición de "Registrarse" como cliente.
En la cual se completan los datos
'''


@bot.callback_query_handler(lambda call: call.data == "opcion-1")
def en_opcion_registrarse(call):
    pass


'''
Encargado de recibir la petición de "Registrar un paquete" como cliente
'''


@bot.callback_query_handler(lambda call: call.data == "opcion-2")
def en_registrar_paquete(call):
    pregunta = '¿A quién le vas a enviar el paquete?'
    markup = telebot.types.ForceReply(selective=False)
    bot.send_message(call.message.chat.id, pregunta, reply_markup=markup)


'''
Encargado de recibir la respuesta a la pregunta "¿A quién le vas a enviar el paquete?"
'''


@bot.message_handler(func=lambda message: message.reply_to_message != None and message.reply_to_message.text == "¿A quién le vas a enviar el paquete?")
def en_registrar_paquete_remitente(mensaje):
    bot.send_chat_action(mensaje.chat.id, 'typing')
    paquete = logic.obtener_paquete_creacion(mensaje.from_user.id)
    datos = {'nombre_remitente': mensaje.text}
    logic.actualizar_datos_paquete(paquete, datos)
    pregunta = '¿En kilogramos cuánto pesa tu paquete?'
    markup = telebot.types.ForceReply(selective=False)
    bot.send_message(mensaje.chat.id, pregunta, reply_markup=markup)


'''
Encargado de recibir la respuesta a la pregunta "¿En kilogramos cuánto pesa tu paquete?"
'''


@bot.message_handler(func=lambda message: message.reply_to_message != None and message.reply_to_message.text == "¿En kilogramos cuánto pesa tu paquete?")
def en_registrar_paquete_peso(mensaje):
    bot.send_chat_action(mensaje.chat.id, 'typing')
    print(validadores.es_numero(mensaje.text))
    if validadores.es_numero(mensaje.text) and float(mensaje.text) > 0:
        paquete = logic.obtener_paquete_creacion(mensaje.from_user.id)
        datos = {'peso_kg': mensaje.text}
        logic.actualizar_datos_paquete(paquete, datos)
        pregunta = '¿A qué dirección quieres mandar el paquete?'
        markup = telebot.types.ForceReply(selective=False)
        bot.send_message(mensaje.chat.id, pregunta, reply_markup=markup)
    else:
        bot.send_message(mensaje.chat.id, "El valor ingresado debe ser un número mayor a cero \U00002639. Te vuelvo a preguntar")
        pregunta = '¿En kilogramos cuánto pesa tu paquete?'
        markup = telebot.types.ForceReply(selective=False)
        bot.send_message(mensaje.chat.id, pregunta, reply_markup=markup)

'''
Encargado de recibir la respuesta a la pregunta "¿A qué dirección quieres mandar el paquete?"
'''


@bot.message_handler(func=lambda message: message.reply_to_message != None and message.reply_to_message.text == "¿A qué dirección quieres mandar el paquete?")
def en_registrar_paquete_direccion_envio(mensaje):
    bot.send_chat_action(mensaje.chat.id, 'typing')
    paquete = logic.obtener_paquete_creacion(mensaje.from_user.id)
    datos = {'direccion_destino': mensaje.text}
    logic.actualizar_datos_paquete(paquete, datos)
    pregunta = '¿En qué dirección quieres que recojamos el paquete?'
    markup = telebot.types.ForceReply(selective=False)
    bot.send_message(mensaje.chat.id, pregunta, reply_markup=markup)


'''
Encargado de recibir la respuesta a la pregunta "¿En qué dirección quieres que recojamos el paquete?"
'''


@bot.message_handler(func=lambda message: message.reply_to_message != None and message.reply_to_message.text == "¿En qué dirección quieres que recojamos el paquete?")
def en_registrar_paquete_direccion_recogida(mensaje):
    bot.send_chat_action(mensaje.chat.id, 'typing')
    paquete = logic.obtener_paquete_creacion(mensaje.from_user.id)
    datos = {'direccion_recogida': mensaje.text, 'estado_actual': Estado.ESTADO_GENERADO,
             'creado_el': datetime.now(), 'fecha_estado_actual': datetime.now(), 'numero_guia': logic.generar_numero_guia()}
    logic.actualizar_datos_paquete(paquete, datos)
    respuesta = "Hemos registrado tu paquete exitosamente \U0001F603"
    bot.send_message(mensaje.chat.id, respuesta)


'''
Encargado de recibir la petición de "Listar mis paquetes" como cliente
'''


@bot.callback_query_handler(lambda call: call.data == "opcion-3")
def en_listar_mis_paquetes(call):
    pass


'''
Encargado de recibir la petición de "Rastrear un paquete" como cliente
'''


@bot.callback_query_handler(lambda call: call.data == "opcion-4")
def en_rastrear_un_paquete(call):
    pass


'''
Encargado de recibir la petición de "Cancelar un paquete" como cliente
'''


@bot.callback_query_handler(lambda call: call.data == "opcion-5")
def en_cancelar_un_paquete(call):
    pass


'''
Encargado de recibir la petición de "Listar paquetes" como usuario
'''


@bot.callback_query_handler(lambda call: call.data == "opcion-6")
def en_listar_paquetes(call):
    pass


'''
Encargado de recibir la petición de "Cambiar estado a un paquete" como usuario
'''


@bot.callback_query_handler(lambda call: call.data == "opcion-7")
def en_cambiar_estado_paquete(call):
    markup = logic.construir_opciones_estado()
    bot.send_message(call.message.chat.id,
                     text="¿A qué estado quieres cambiar el paquete?", reply_markup=markup)
    pass


'''
Encargado de recibir la respuesta del a estado a "Cambiar estado a un paquete" como usuario
'''


@bot.callback_query_handler(lambda call: call.message != None and call.message.text == "¿A qué estado quieres cambiar el paquete?")
def en_cambiar_estado_paquete_estado(call):
    print(call.data)
    pass


'''
Encargado de recibir la petición de "Eliminar estado de un paquete" como usuario
'''


@bot.callback_query_handler(lambda call: call.data == "opcion-8")
def en_eliminar_estado_paquete(call):
    pass


'''
Mensaje por efecto
'''


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
