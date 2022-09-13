from pathlib import Path

BASE_FILE_DIR = Path('/tmp')
ROOT_DIR = Path().resolve()
#parent atributo que hace referencia al directorio principal.
SQL_DIR = ROOT_DIR / "sql"
CATEGORY_DIR = ROOT_DIR / "categories"


RAW_TABLE_NAME = "raw"
CATEGORY_TABLE_NAME = "records_category"
SOURCE_TABLE_NAME = "records_source"
PROVINCE_CATEGORY = "records_province_category"
TEATRO_TABLE_NAME =  "teatro"

TABLE_NAMES = [
        RAW_TABLE_NAME,
        CATEGORY_TABLE_NAME,
        SOURCE_TABLE_NAME,
        PROVINCE_CATEGORY,
        TEATRO_TABLE_NAME        
]