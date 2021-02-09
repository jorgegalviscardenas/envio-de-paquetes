from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine (
    'sqlite:///database/envio_paquetes.sqlite',
    echo=False,
    connect_args = {'check_same_thread': False})

Base = declarative_base()
Session = sessionmaker(bind=engine)

session = Session()