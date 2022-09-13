CREATE TABLE records_source
(
    records_source_id INTEGER PRIMARY KEY NOT NULL,
    fuente VARCHAR(200),
    cantidad INTEGER,
    fecha_de_carga DATE
);