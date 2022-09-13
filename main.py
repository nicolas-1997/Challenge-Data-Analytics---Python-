# Python
from datetime import datetime
import pandas as pd


#Utilidad
from logs import logger
# Modulos
from constants import *
from config import categories
from ET import *

def run():
    for categoria in categories:
      newdf = ExtractUrl(categoria["url"], categoria["name"])
      logger.info(categoria["name"])
      csv = newdf.extract("2022-09-12")
      try:
        df = pd.read_csv(csv, encoding="utf-8")
        print(df.columns)
      except(Exception) as e:
        logger.error(e)

if __name__ == "__main__":
    run()
