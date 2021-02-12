import database.db as db
from sqlalchemy import Column, String, Float, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship 
import telebot
class Usuario(db.Base):
    __tablename__ 	= 'usuario'

    id	= Column('id', String(15), primary_key=True, nullable=False)  
    nombres = Column('nombres', String(50), nullable=False) 
    apellidos = Column('apellidos', String(50), nullable=False) 
    documento = Column('documento', String(20), nullable=False,unique=True) 
    email = Column('email', String(200), nullable=False) 
    eventos_creados = relationship("Evento", back_populates="usuario")
    def __init__ (self, id, nombre, documento,email): 
        self.id = id
        self.nombre = nombre 
        self.documento = documento
        self.email = email

    def __repr__ (self):
        return f"<Usuario {self.id}>"
    '''
    Se encarga de construir el menú como usuario del sistema
    @return InlineKeyboardMarkup contenedor de las opciones
    '''
    def construir_menu(self):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Listar paquetes', callback_data="opcion-6"))
        markup.add(telebot.types.InlineKeyboardButton(text='Cambiar estado a un paquete', callback_data="opcion-7"))
        markup.add(telebot.types.InlineKeyboardButton(text='Eliminar estado de un paquete', callback_data="opcion-8"))
        return markup