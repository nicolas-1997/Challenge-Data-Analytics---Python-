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

        self.date = datetime.strptime(date, "%Y-%m-%d").date()
        file_path = self.file_path_crib.format(
            category=self.name, year=self.date.year, month=self.date.month, day=self.date.day)

        self.dir_path = CATEGORY_DIR / file_path
        self.dir_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            r = requests.get(self.url)
            r.content.decode('utf-8')
            logger.info("La request se realizo correctamente.")

            with open(self.dir_path, "w", encoding="utf-8") as f:
                f.write(r.text)

            return self.dir_path
        except (Exception) as e:
            logger.error(e)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """_summary_

        Args:
            df (pd.DataFrame): _description_

        Returns:
            pd.DataFrame: _description_
        """

        rename_columns = {
            'cod_loc': 'cod_localidad',
            'id_prov': 'id_provincia',
            'id_departamento': 'id_departamento',
            'categoria': 'categoria',
            'provincia': 'provincia',
            'localidad': 'localidad',
            'nombre': 'nombre',
            'domicilio': 'domicilio',
            'CP': ' codigo_posta',
            'telefono': 'numero_de_telefono',
            'mail': 'mail',
            'web': 'web'
        }

        df = df.rename(columns=rename_columns)

        column_list = [
            'cod_localidad',
            'id_provincia',
            'id_departamento',
            'categoria',
            'provincia',
            'localidad',
            'nombre',
            'domicilio',
            'codigo_posta',
            'numero_de_telefono',
            'mail',
            'web'
        ]

        return df[column_list]


class ExtractMuseo(ExtractUrl):

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        rename_columns = {
            'cod_loc': 'cod_localidad',
            'id_prov': 'id_provincia',
            'id_departamento': 'id_departamento',
            'categoria': 'categoria',
            'provincia': 'provincia',
            'localidad': 'localidad',
            'nombre': 'nombre',
            'domicilio': 'domicilio',
            'CP': ' codigo_posta'
        }