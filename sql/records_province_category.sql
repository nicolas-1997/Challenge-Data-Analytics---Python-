CREATE TABLE records_province_category
(
    records_province_category_id INTEGER PRIMARY KEY NOT NULL,
    provincia VARCHAR(120),
    categoria VARCHAR(120),
    cantidad INTEGER,
    fecha_de_carga DATE
)