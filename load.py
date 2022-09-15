from sqlalchemy import create_engine
from config import *
import pandas as pd 
from constants import *
from logs import logger


engine = create_engine(DATABASE_LOCATION)

class Load():

    def load(self, df):
        logger.info(f"comenzando la carga de {self.table_name}")
        df.to_sql(self.table_name, con=engine, index=False, if_exists="replace")
        logger.info(f"Termino la carga de {self.table_name}")


class RawLoad(Load):
    table_name = RAW_TABLE_NAME

    def load_table(self, file_path):
        df = pd.read_csv(file_path)
        return super().load(df)


class TeatroLoader(Load):

    table_name = TEATRO_TABLE_NAME
        
    def load_table(self, file_path):
        df = pd.read_csv(file_path)

        insigth_df = df.groupby("provincia", as_index=False).count()[
            ["provincia", "capacidad", "actividad_especifica", "inicio_act"]
        ]
        return super().load(insigth_df)

    


class CategoryLoader(Load):

    table_name = CATEGORY_TABLE_NAME

    def load_table(self, file_path):
        
        df = pd.read_csv(file_path)
        category_df  = df.groupby(["categoria"], as_index=False).size()
        
        return super().load(category_df)



class SourceLoader(Load):
    table_name = SOURCE_TABLE_NAME
    def load_table(self, file_paths):
        
        lista =  list()
        for name, file_path in file_paths.items():
            df = pd.read_csv(file_path)
            lista.append({"source":name, "count": df.size})

        df_source = pd.DataFrame(lista)
        
        return super().load(df_source)


class ProvCatLoader(Load):
    table_name = PROVINCE_CATEGORY
    
    def load_table(self, file_path):
            
        df = pd.read_csv(file_path)

        df_cat_prov = df.groupby(
            ["categoria", "provincia"], as_index=False
        ).size()
        
        
        return super().load(df_cat_prov)
