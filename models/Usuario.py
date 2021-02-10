import database.db as db
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship 

class Usuario(db.Base):
    __tablename__ 	= 'usuario'

    id	= Column('id', Integer, primary_key=True, autoincrement=True) 
    codigo = Column('codigo', String(15), nullable=False,unique=True) 
    nombre = Column('nombre', String(50), nullable=False) 
    documento = Column('documento', String(20), nullable=False,unique=True) 
    email = Column('email', String(200), nullable=False) 
    
    def __init__ (self, codigo, nombre, documento,email): 
        self.codigo = codigo
        self.nombre = nombre 
        self.documento = documento
        self.email = email

    def __repr__ (self):
        return f"<Usuario {self.id}>"