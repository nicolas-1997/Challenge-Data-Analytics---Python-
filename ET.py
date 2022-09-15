import pandas as pd
import requests
from datetime import datetime
import csv
# Modulos
from logs import logger
from constants import *


class ExtractUrl():

    def __init__(self, url, name) -> None:
        self.url = url
        self.name = name
        self.file_path_crib = (
            "{category}/{year}-{month:02d}/{category}-{day:02d}-{month:02d}-{year}.csv")

    def extract(self, date: str) -> str:
        """_summary_

        Args:
            date (str): Fecha de corrida -> yyyy-mm-dd.

        Returns:
            str: _description_
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
        
        silver_df = df.rename(columns=rename_columns)

        return silver_df[new_column_list]
