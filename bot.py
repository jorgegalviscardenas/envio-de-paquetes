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

RESPUESTA_OK = "OK"
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
def en_registrarse(call):
    pregunta = '¿Cuál es tu número de documento?'
    markup = telebot.types.ForceReply(selective=False)
    bot.send_message(call.message.chat.id, pregunta, reply_markup=markup)


'''
Encargado de recibir la respuesta a la pregunta "¿Cuál es tu número de documento?"
'''


@bot.message_handler(func=lambda message: message.reply_to_message != None and message.reply_to_message.text == "¿Cuál es tu número de documento?")
def en_registrarse_documento(mensaje):
    bot.send_chat_action(mensaje.chat.id, 'typing')
    if validadores.contiene_solo_numeros(mensaje.text):
        cliente = logic.obtener_cliente_registro(mensaje.from_user.id)
        datos = {'documento': mensaje.text}
        logic.actualizar_datos_modelo(cliente, datos)
        pregunta = '¿Cuál es tu número de teléfono?'
        markup = telebot.types.ForceReply(selective=False)
        bot.send_message(mensaje.chat.id, pregunta, reply_markup=markup)
    else:
        bot.send_message(
            mensaje.chat.id, "El número de documento solo debe contener números \U00002639. Te vuelvo a preguntar")
        pregunta = '¿Cuál es tu número de documento?'
        markup = telebot.types.ForceReply(selective=False)
        bot.send_message(mensaje.chat.id, pregunta, reply_markup=markup)


'''
Encargado de recibir la respuesta a la pregunta "¿Cuál es tu número de teléfono?"
'''


@bot.message_handler(func=lambda message: message.reply_to_message != None and message.reply_to_message.text == "¿Cuál es tu número de teléfono?")
def en_registrarse_telefono(mensaje):
    bot.send_chat_action(mensaje.chat.id, 'typing')
    if validadores.contiene_solo_numeros(mensaje.text):
        cliente = logic.obtener_cliente_registro(mensaje.from_user.id)
        datos = {'telefono': mensaje.text}
        logic.actualizar_datos_modelo(cliente, datos)
        pregunta = '¿Cuál es tu email?'
        markup = telebot.types.ForceReply(selective=False)
        bot.send_message(mensaje.chat.id, pregunta, reply_markup=markup)
    else:
        bot.send_message(
            mensaje.chat.id, "El número de teléfono solo debe contener números \U00002639. Te vuelvo a preguntar")
        pregunta = '¿Cuál es tu número de teléfono?'
        markup = telebot.types.ForceReply(selective=False)
        bot.send_message(mensaje.chat.id, pregunta, reply_markup=markup)

'''
Encargado de recibir la respuesta a la pregunta "¿Cuál es tu email?"
'''


@bot.message_handler(func=lambda message: message.reply_to_message != None and message.reply_to_message.text == "¿Cuál es tu email?")
def en_registrarse_email(mensaje):
    bot.send_chat_action(mensaje.chat.id, 'typing')
    if validadores.es_email(mensaje.text):
        cliente = logic.obtener_cliente_registro(mensaje.from_user.id)
        datos = {'email': mensaje.text}
        logic.actualizar_datos_modelo(cliente, datos)
        respuesta = "Hemos completado tu registro exitosamente \U0001F603. Ejecuta el comando /menu para ver las nuevas opciones."
        bot.send_message(mensaje.chat.id, respuesta)
    else:
        bot.send_message(
            mensaje.chat.id, "La dirección de email ingresada no es válida \U00002639. Te vuelvo a preguntar")
        pregunta = '¿Cuál es tu email?'
        markup = telebot.types.ForceReply(selective=False)
        bot.send_message(mensaje.chat.id, pregunta, reply_markup=markup)

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
    logic.actualizar_datos_modelo(paquete, datos)
    pregunta = '¿En kilogramos cuánto pesa tu paquete?'
    markup = telebot.types.ForceReply(selective=False)
    bot.send_message(mensaje.chat.id, pregunta, reply_markup=markup)


'''
Encargado de recibir la respuesta a la pregunta "¿En kilogramos cuánto pesa tu paquete?"
'''


@bot.message_handler(func=lambda message: message.reply_to_message != None and message.reply_to_message.text == "¿En kilogramos cuánto pesa tu paquete?")
def en_registrar_paquete_peso(mensaje):
    bot.send_chat_action(mensaje.chat.id, 'typing')
    if validadores.es_numero(mensaje.text) and float(mensaje.text) > 0:
        paquete = logic.obtener_paquete_creacion(mensaje.from_user.id)
        datos = {'peso_kg': mensaje.text}
        logic.actualizar_datos_modelo(paquete, datos)
        pregunta = '¿A qué dirección quieres mandar el paquete?'
        markup = telebot.types.ForceReply(selective=False)
        bot.send_message(mensaje.chat.id, pregunta, reply_markup=markup)
    else:
        bot.send_message(
            mensaje.chat.id, "El peso ingresado debe ser un número mayor a cero \U00002639. Te vuelvo a preguntar")
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
    logic.actualizar_datos_modelo(paquete, datos)
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
    fecha = datetime.now()
    datos = {'direccion_recogida': mensaje.text, 'estado_actual': Estado.ESTADO_GENERADO,
             'creado_el': fecha, 'fecha_estado_actual': fecha, 'numero_guia': logic.generar_numero_guia()}
    logic.actualizar_datos_modelo(paquete, datos)
    logic.crear_evento_generado(paquete.id,fecha,fecha)
    respuesta = f"Hemos registrado tu paquete exitosamente \U0001F603. El número de guía es: *{paquete.numero_guia}*"
    bot.send_message(mensaje.chat.id, respuesta,parse_mode="Markdown")


'''
Encargado de recibir la petición de "Listar mis paquetes" como cliente
'''


@bot.callback_query_handler(lambda call: call.data == "opcion-3")
def en_listar_mis_paquetes(call):
    paquetes = logic.listar_mis_paquetes(call.message.chat.id)

    if len(paquetes) == 0 :
        bot.send_message(call.message.chat.id, f"Usted no ha registrado paquetes \U0001F609")
        return

    text = ""
    for paq in paquetes:
        text += f"*Fecha de creación:* {paq.creado_el} \n"
        text += f"*Dirección de destino:* {paq.direccion_destino} \n"
        text += f"*Remitente:* {paq.nombre_remitente} \n"
        text += f"*Estado actual:* {paq.estado_actual_objeto.nombre} \n"
        text += f"*Fecha del estado actual:* {paq.fecha_estado_actual} \n\n"
    bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
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
    markup = telebot.types.ForceReply(selective=False)
    bot.send_message(call.message.chat.id, text="Digite el número de guía del paquete que desea cancelar", reply_markup=markup)

'''
Encargado de recibir la respuesta de "Digite el número de guía del paquete que desea cancelar"
'''

@bot.message_handler(func=lambda message: message.reply_to_message != None and message.reply_to_message.text == "Digite el número de guía del paquete que desea cancelar")
def en_cancelar_paquete(message):
    nguia = message.text
    resp = logic.evento_paquete_guia(message.chat.id, nguia)
    if resp == RESPUESTA_OK:
        markup = logic.construir_opciones_estado()
        bot.send_message(message.chat.id, f"\U00002705 Paquete eliminado correctamente.", parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, resp, parse_mode="Markdown")



'''
Encargado de recibir la petición de "Listar paquetes" como usuario
'''


@bot.callback_query_handler(lambda call: call.data == "opcion-6")
def en_listar_paquetes(call):
    paquetes = logic.listar_paquetes()

    if len(paquetes) == 0 :
        bot.send_message(call.message.chat.id, f"No se encuentran paquetes sin entregar \U0001F609")
        return

    text = ""
    total = 0
    for paq in paquetes:
        text += f"*Fecha de creación:* {paq.creado_el} \n"
        text += f"*Número de guía:* {paq.numero_guia} \n"
        text += f"*Estado:* {paq.estado_actual_objeto.nombre} \n"
        text += f"*Documento de identidad:* {paq.cliente.documento} \n"
        text += f"*Cliente:* {paq.cliente.nombres} {paq.cliente.apellidos} \n\n"
        total += 1

    text += f"*Total de paquetes:* {total}"

    bot.send_message(call.message.chat.id, text, parse_mode="Markdown")


'''
Encargado de recibir la petición de "Cambiar estado a un paquete" como usuario
'''


@bot.callback_query_handler(lambda call: call.data == "opcion-7")
def en_cambiar_estado_paquete(call):
    markup = telebot.types.ForceReply(selective=False)
    bot.send_message(call.message.chat.id, text="Digite el número de guía del paquete al que deseas cambiar el estado", reply_markup=markup)

'''
Encargado de recibir la respuesta de "Digite el número de guía del paquete al que deseas cambiar el estado"
'''

@bot.message_handler(func=lambda message: message.reply_to_message != None and message.reply_to_message.text == "Digite el número de guía del paquete al que deseas cambiar el estado")
def en_cambiar_estado_paquete_guia(message):
    nguia = message.text
    resp = logic.evento_paquete_guia(message.chat.id, nguia)
    if resp == RESPUESTA_OK:
        markup = logic.construir_opciones_estado()
        bot.send_message(message.chat.id, text="¿A qué estado quieres cambiar el paquete?", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, resp, parse_mode="Markdown")


'''
Encargado de recibir la respuesta de "¿A qué estado quieres cambiar el paquete?"
'''

@bot.callback_query_handler(lambda call: call.message != None and call.message.text == "¿A qué estado quieres cambiar el paquete?")
def en_cambiar_estado_paquete_estado(call):
    markup = telebot.types.ForceReply(selective=False)
    resp = logic.update_evento_estado_id(call.message.chat.id, call.data)
    if resp == RESPUESTA_OK:
        bot.send_message(call.message.chat.id, text="¿Cuál es la fecha y la hora en la que se cambió de estado el paquete?(YYYY-MM-DD HH:mm)", reply_markup=markup)
    else:
        bot.send_message(call.message.chat.id, resp, parse_mode="Markdown")

'''
Encargado de recibir la respuesta de "¿Cuál es la fecha y la hora en la que se cambió de estado el paquete?(yyyy-MM-dd HH:mm)"
'''

@bot.message_handler(func=lambda message: message.reply_to_message != None and message.reply_to_message.text == "¿Cuál es la fecha y la hora en la que se cambió de estado el paquete?(yyyy-MM-dd HH:mm)")
def en_cambiar_estado_paquete_fecha(message):
    parts = re.match(
        r"^([0-9]{4})-([0-9]{1,2})-([0-9]{1,2}) ([0-9]{1,2}):([0-9]{1,2})$", 
        message.text,
        re.IGNORECASE)
    resp = logic.update_evento_fecha(message.chat.id, parts)
    if resp == RESPUESTA_OK:
        bot.send_message(message.chat.id, f"\U00002705 Se ha cambiado el estado del paquete con éxito.", parse_mode="Markdown")
    else:
        bot.reply_to(message, resp, parse_mode="Markdown")
        bot.send_message(message.chat.id, text="¿Cuál es la fecha y la hora en la que se cambió de estado el paquete?(YYYY-MM-DD HH:mm)", reply_markup=telebot.types.ForceReply(selective=False))


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
