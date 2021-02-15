import database.db as db
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship


class Evento(db.Base):
    __tablename__ = 'evento'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    fecha = Column('fecha', DateTime, nullable=True)
    creado_el = Column('creado_el', DateTime,
                       server_default=func.now(), nullable=True)

    estado_id = Column('estado_id', Integer, ForeignKey(
        'estado.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=True)
    estado = relationship("Estado", back_populates="eventos")

    creado_por = Column('creado_por', String(15), ForeignKey(
        'usuario.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    usuario = relationship("Usuario", back_populates="eventos_creados")

    paquete_id = Column('paquete_id', Integer, ForeignKey(
        'paquete.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    paquete = relationship("Paquete", back_populates="eventos")

    def __init__(self, fecha, creado_el, estado_id, creado_por, paquete_id):
        self.fecha = fecha
        self.creado_el = creado_el
        self.estado_id = estado_id
        self.creado_por = creado_por
        self.paquete_id = paquete_id

    def __repr__(self):
        return f"<Evento {self.id}>"
