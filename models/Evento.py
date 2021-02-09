import database.db as db
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship 

class Evento(db.Base):
    __tablename__ 	= 'evento'

    id	= Column('id', Integer, primary_key=True, autoincrement=True) 
    fecha	= Column('fecha', DateTime, nullable=True)
    creado_el	= Column('creado_el', DateTime, server_default=func.now(), nullable=True)
 
    estado_id = Column('estado_id', String(15), ForeignKey('estado.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    estados	= relationship("Estado", back_populates="eventos_estado")
    
    creado_por = Column('creado_por', String(15), ForeignKey('usuario.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    usuarios   = relationship("Usuario", back_populates="eventos_usuario")

    def __init__ (self, fecha, creado_el, estado_id): 
        self.fecha = fecha
        self.creado_el = creado_el 
        self.estado_id = estado_id

    def __repr__ (self):
        return f"<Evento {self.id}>"