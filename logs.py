import logging
import os
os.makedirs('logs/', exist_ok=True)
formato = ' [%(asctime)s], %(levelname)s, %(message)s, %(filename)s:%(lineno)d'
logging.basicConfig(filename='./logs/loggers.log', level=logging.INFO, format=formato, encoding='utf-8')

# CONSOLE
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

logger = logging.getLogger()