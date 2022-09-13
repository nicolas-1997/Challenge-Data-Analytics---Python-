from decouple import AutoConfig
from constants import ROOT_DIR

config = AutoConfig(search_path=ROOT_DIR)


##DB Conection 

DATABASE_INFO = {"host":config('DB_HOST',default='localhost'),
                 "port":config('DB_PORT',default='5432'),
                 "user":config('DB_USER',default='User1'),
                 "password":config('DB_PASSWORD',default='123456'),
                 "dbname":config('DB_NAME',default='challenge_data_analytics')}

DATABASE_LOCATION = f"postgresql://{DATABASE_INFO['user']}:{DATABASE_INFO['password']}@{DATABASE_INFO['host']}:{DATABASE_INFO['port']}/{DATABASE_INFO['dbname']}"



#Levantar las variables de Settings.ini
URL_MUSEO = config("URL_MUSEOS")
URL_TEATROS = config("URL_TEATROS")
URL_BIBLIOTECAS = config("URL_BIBLIOTECAS")


categories = [
    {
        "name":"museos",
        "url": URL_MUSEO
    },
     {
        "name":"teatros",
        "url": URL_TEATROS
    },
     {
        "name":"bibliotecas",
        "url": URL_BIBLIOTECAS
    }
]