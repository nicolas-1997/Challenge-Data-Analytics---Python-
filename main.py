# Python
import os
import pandas as pd
import click
from datetime import date
#Utilidad
from logs import logger
# Modulos
from constants import *
from config import categories
from ET import *
from load import *

extractor_dic = {
  'museos': ExtractUrl(categories[0]["url"], categories[0]["name"]),
  'teatros': ExtractUrl(categories[1]["url"], categories[1]["name"]),
  'bibliotecas': ExtractUrl(categories[2]["url"], categories[2]["name"])
}



def extract(date:str) -> dict:
  """_summary_

  Args:
      date (str): Fecha de corrida -> yyyy-mm-dd.

  Returns:
      dict: diccionario con las categorias y los paths a sus archivos csv.
  """
  file_paths_dict = dict()

  for categoria in categories:
    try:
      logger.info(f'Comenzado la extraccion de la url de {categoria["name"]}')
      file_path =  extractor_dic[categoria["name"]].extract(date)
      logger.info("Guardando los path de los archivos.")
      file_paths_dict[categoria["name"]] = file_path
    except Exception as e:
      logger.error(e)
   
  return file_paths_dict

def transform(file_path_list:list, output_path:str, date:str):
  """
  Transform
    Se encarga de llevar los Dataframe por los niveles del etl: Bronce-Silver-Gold
  Args:
      file_path_list (list(str)): Es la lista de los path a los archivos csv en su forma cruda.
      output_path (str): Es el path donde se de desea guardar el archivo csv ya en la capa Gold.
      date (str): Fecha de corrida -> yyyy-mm-dd.
  """
  silver_df_list = list() 
  for name , extractor in extractor_dic.items():
    logger.info(f"Obteniendo el archivo csv: {name} Para su Transformacion")
    try:
      logger.info("Creando el dataframe para nivel Bronce")
      df_bronce = pd.read_csv(file_path_list[name], encoding="utf-8")
      logger.info("Creando el dataframe para nivel Silver")
      silver_df = extractor.transform(df_bronce)
      silver_df_list.append(silver_df)
    except Exception as e:
      logger.error(e)

  logger.info("Creando el dataframe para nivel Gold")
  merge_path = f'{output_path}/merge_df_{date}.csv'
  gold_df = pd.concat(silver_df_list, axis=0)
  logger.info(f"Guardando el DataFrame en: {merge_path}")
  gold_df.to_csv(merge_path)
  return merge_path



@click.command()
@click.option("--date",prompt="Añada una fecha o date pulse enter para el dia de hoy", default=date.today(), help="run day- yyyy-mm-dd")
def run(date:str):
  """
  Run 
    Se encarga de desencadenar todos los procesos de ETL

  Args:
    date (str): Fecha de corrida -> yyyy-mm-dd.
  """
  #Extract.
  logger.info("Comenzando el Proceso de Extract")
  file_path_list = extract(date)
  #Transform.
  logger.info("Comenzando el Proceso de Transform")
  
  output_path = MERGE_DF.format(ROOT_DIR=ROOT_DIR,date=date)
  os.makedirs(output_path, exist_ok=True)
  
  gold_csv_path = transform(file_path_list, output_path, date)

  #Load
  logger.info("Comenzando el proceso de Load")
  try:
      TeatroLoader().load_table(file_path_list["teatros"])
      CategoryLoader().load_table(gold_csv_path)
      SourceLoader().load_table(file_path_list)
      ProvCatLoader().load_table(gold_csv_path)
      RawLoad().load_table(gold_csv_path)

      
  except Exception as e:
    logger.error(e)

  logger.info("La carga de Tablas termino")


if __name__ == "__main__":
    run()
