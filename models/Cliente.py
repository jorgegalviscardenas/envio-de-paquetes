import database.db as db
from sqlalchemy import Column, String, Float, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship 
import telebot
'''
Representa un cliente que envia paquetes

@author Sebastian Noreña Marquez <sebastian.norenam@autonoma.edu.co>
@author Camilo Andres Lengua Duque <camiloa.lenguad@autonoma.eu.co>
@author Alejandro Gomez Alzate <alejandro.gomez@autonoma.edu.co>
@author Jorge Galvis Cárdenas <jorge.galvisc@autonoma.edu.co>

@version 20210211
'''
class Cliente(db.Base):
    __tablename__ 	= 'cliente'

    id	= Column('id', String(15), primary_key=True, nullable=False)  
    nombres = Column('nombres', String(50), nullable=False)
    apellidos = Column('apellidos', String(50), nullable=False)  
    documento = Column('documento', String(20), nullable=True,unique=True) 
    email = Column('email', String(200), nullable=True) 
    telefono = Column('telefono', String(15), nullable=True) 
    paquetes = relationship("Paquete", back_populates="cliente")
    def __init__ (self, id, nombres,apellidos): 
        self.id = id
        self.nombres = nombres 
        self.apellidos = apellidos

    def __repr__ (self):
        return f"<Cliente {self.id}>"
    '''
    Se encarga de construir el menú como cliente. Si el cliente tiene los datos completas le muestra
    las opciones que puede realizar sobre los paquetes, si no lo tiene completo solo le muestra la
    opción de "Registrarse"
    @return InlineKeyboardMarkup contenedor de las opciones
    '''
    def construir_menu(self):
        markup = telebot.types.InlineKeyboardMarkup()
        if(self.documento != None and self.email != None and self.telefono != None):
            markup.add(telebot.types.InlineKeyboardButton(text='Registrar un paquete', callback_data="opcion-2"))
            markup.add(telebot.types.InlineKeyboardButton(text='Listar mis paquetes', callback_data="opcion-3"))
            markup.add(telebot.types.InlineKeyboardButton(text='Rastrear un paquete', callback_data="opcion-4"))
            markup.add(telebot.types.InlineKeyboardButton(text='Cancelar un paquete', callback_data="opcion-5"))
        else:
            markup.add(telebot.types.InlineKeyboardButton(text='Registrarse', callback_data="opcion-1"))
        return markup
