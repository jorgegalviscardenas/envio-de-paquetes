import database.db as db 
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
class Estado(db.Base):
    __tablename__ = 'estado'

    id	= Column('id', Integer, primary_key=True, nullable=False) 
    nombre = Column('nombre', String(100), nullable=False) 
    orden  = Column('orden', Integer, nullable=False) 
    eventos = relationship("Evento", back_populates="estado")
    paquetes_estado_actual = relationship("Paquete", back_populates="estado_actual_objeto")
    def __init__ (self, id, nombre,orden=1): 
        self.id = id
        self.nombre = nombre
        self.orden  = orden

    def __repr__ (self):
        return f"<Estado {self.id}>"