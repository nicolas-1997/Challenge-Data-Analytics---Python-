import pandas as pd
import requests
from datetime import datetime
import csv
# Modulos
from logs import logger
from constants import *


class ExtractUrl():

    def __init__(self, url, name) -> None:
        """ExtractUrl se encarga de ejecutar dos procesos, Extract y Transform

        Args:
            url (str): Acceso a la fuente de datos.
            name (_type_): nombre de la categoria de datos.
        """
        self.url = url
        self.name = name
        self.file_path_crib = (
            "{category}/{year}-{month:02d}/{category}-{day:02d}-{month:02d}-{year}.csv")

    def extract(self, date: str) -> str:
        """Extract
        Description:
            Se encarga de extraer el csv de la url crear su path y retornar este.

        Args:
            date (str): Fecha de corrida -> yyyy-mm-dd.

        Returns:
            str: Retorna el path al archivo que se acabo de crear
        """
        self.date = datetime.strptime(date, "%Y-%m-%d").date()
        file_path = self.file_path_crib.format(
            category=self.name, year=self.date.year, month=self.date.month, day=self.date.day)

        self.dir_path = CATEGORY_DIR / file_path
        self.dir_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            r = requests.get(self.url)
            r.encoding = 'utf-8'
            logger.info("La request se realizo correctamente.")

            with open(self.dir_path, "w", encoding="utf-8") as f:
                f.write(r.text)

            return self.dir_path
        except (Exception) as e:
            logger.error(e)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:

        """Transform
        
        Description:
            Se encarga de transformar los dataframes, de Normalizar sus columnas.

        Args:
            pd (pd.DataFrame): Es el objeto Dataframe para su limpieza y normalizaciom
        Returns:
            pd (pd.DataFrame): Retorna el DataFrame limpio y solo con las columnas que necesitamos.
        """


        new_column_list = ['cod_localidad', 'id_provincia', 'id_departamento', 'categoria', 'provincia',
                           'localidad', 'nombre', 'domicilio', 'codigo_postal', 'numero_de_telefono', 'mail', 'web']
        old_column_list = ['cod_loc', 'id_provincia', 'id_departamento', 'categoria',
                           'provincia', 'localidad', 'nombre', 'domicilio', 'cp', 'telefono', 'mail', 'web']

        rename_columns = dict()

        if self.name == "teatros":
            old_column_list[1] = "id_prov"
            old_column_list[8] = "CP"

        elif self.name == "bibliotecas":
            old_column_list = [x.capitalize() for x in old_column_list]
            old_column_list[0] = "Cod_Loc"
            old_column_list[1] = "IdProvincia"
            old_column_list[2] = "IdDepartamento"
            old_column_list[3] = "Categoría"
            old_column_list[8] = "CP"
            old_column_list[9] = "Teléfono"


        for i in range(len(old_column_list)):
            rename_columns[old_column_list[i]] = new_column_list[i]
        

        logger.info("Se han normalizado los nombres de las columnas")
        silver_df = df.rename(columns=rename_columns)
        logger.info("El nuevo data frame se creo correctamente.")
        return silver_df[new_column_list]
