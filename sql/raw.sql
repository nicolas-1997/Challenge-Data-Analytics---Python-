CREATE TABLE IF NOT EXISTS raw(
    job_date DATE PRIMARY KEY,
    cod_localidad INTEGER NOT NULL,
    id_provincia INTEGER NOT NULL,
    id_departamento INTEGER NOT NULL,
    categoria VARCHAR(255) NOT NULL,
    provincia VARCHAR(255) NOT NULL,
    localidad VARCHAR(255) NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    domicilio VARCHAR(255) NOT NULL,
    codigo_postal VARCHAR(255) NOT NULL,
    numero_de_telefono VARCHAR(255) NOT NULL,
    mail VARCHAR(255) NOT NULL,
    web VARCHAR(255) NOT NULL
);