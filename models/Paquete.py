import database.db as db
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship 

class Paquete(db.Base):
    __tablename__ 	= 'paquete'

    id	               = Column('id', Integer, primary_key=True, autoincrement=True) 
    numero_guia        = Column('numero_guia', String(20), nullable=False,unique=True) 
    nombre_remitente   = Column('nombre_remitente', String(100), nullable=True) 
    peso_kg            = Column('peso_kg', Float(10,2), nullable=True) 
    direccion_destino  = Column('direccion_destino', String(200), nullable=True) 
    direccion_recogida = Column('direccion_recogida', String(200), nullable=True)    
    fecha_estado_actual= Column('fecha_estado_actual', DateTime, server_default=func.now(), nullable=True)
    creado_el	       = Column('creado_el', DateTime, server_default=func.now(), nullable=True)

    cliente_id = Column('cliente_id', String(15), ForeignKey('cliente.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    cliente	= relationship("Cliente", back_populates="paquetes")
    
    estado_actual = Column('estado_actual', String(15), ForeignKey('estado.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=True)
    estado_actual_objeto	= relationship("Estado", back_populates="paquetes_estado_actual")
    eventos = relationship("Evento", back_populates="paquete")
    def __init__ (self, numero_guia, nombre_remitente, peso_kg,direccion_destino,direccion_recogida,fecha_estado_actual): 
        self.numero_guia = numero_guia
        self.nombre_remitente = nombre_remitente 
        self.peso_kg = peso_kg
        self.direccion_destino = direccion_destino
        self.direccion_recogida= direccion_recogida
    def __repr__ (self):
        return f"<Paquete {self.id}>"