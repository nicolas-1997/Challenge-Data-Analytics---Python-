from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy_utils import database_exists, create_database
from constants import *
from config import DATABASE_LOCATION
from logs import logger

createEngine = create_engine(DATABASE_LOCATION)


def create_db():
    db_exists = database_exists(createEngine.url)
    if not db_exists:
        create_database(createEngine.url)
        logger.info("Creando la Base de Datos")
    else:
        logger.info("La Base de Datos ya existe")
    


def create_table():
    """
    Create table

    - Description:
        - crea las tablas de la base de datos.

    - Parameters:
        - Ninguno.
    
    - Return:
        - Nada.
    """

    with createEngine.connect() as c:
        for file in TABLE_NAMES:
            logger.info(f'Creando Tabla: {file}')
            with open(SQL_DIR/ f'{file}.sql') as f:
                query = text(f.read())
                c.execute(f"DROP TABLE IF EXISTS {file}")
                c.execute(query)
                logger.info(f'La Tabla {file} se creo correctamente.')



if __name__ == "__main__":
    try:
        create_db()
        create_table()  
    except(Exception) as e:
        logger.error(e)