import database.db as db 
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
'''
Representa un estado que puede tomar un evento y el estado actual de un paquete

@author Sebastian Noreña Marquez <sebastian.norenam@autonoma.edu.co>
@author Camilo Andres Lengua Duque <camiloa.lenguad@autonoma.eu.co>
@author Alejandro Gomez Alzate <alejandro.gomez@autonoma.edu.co>
@author Jorge Galvis Cárdenas <jorge.galvisc@autonoma.edu.co>

@version 20210211
'''
class Estado(db.Base):
    '''
    @var string Nombre de la tabla asociada al modelo
    '''
    __tablename__ = 'estado'
    '''
    @var integer Identificador en la base de datos
    '''
    id	= Column('id', Integer, primary_key=True, nullable=False) 
    '''
    @var string Nombre del estado
    '''
    nombre = Column('nombre', String(100), nullable=False) 
    '''
    @var integer Orden en el que deben aparecer los estados
    '''
    orden  = Column('orden', Integer, nullable=False) 
    '''
    @var [Evento] Listado de eventos que tienen este estado
    '''
    eventos = relationship("Evento", back_populates="estado")
    '''
    @var [Paquete] Listado de paquetes que tienen este estado
    '''
    paquetes_estado_actual = relationship("Paquete", back_populates="estado_actual_objeto")
    ESTADO_GENERADO = 1
    '''
    Constructor
    @param integer id Identificador del estado
    @param string nombre Nombre del estado
    @param integer ordern Orden que sigue el estado
    '''
    def __init__ (self, id, nombre,orden=1): 
        self.id = id
        self.nombre = nombre
        self.orden  = orden

    def __repr__ (self):
        return f"<Estado {self.id}>"