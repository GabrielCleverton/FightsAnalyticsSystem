# src/database/schema.py

INSTRUCOES_CRIACAO = """
    CREATE TABLE IF NOT EXISTS lutas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        video_nome TEXT NOT NULL,
        data_processamento DATETIME DEFAULT CURRENT_TIMESTAMP,
        vencedor_detectado TEXT
    );

    CREATE TABLE IF NOT EXISTS raw_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        luta_id INTEGER,
        frame_numero INTEGER,
        person_id INTEGER,
        angulo_cotovelo_dir REAL,
        angulo_cotovelo_esq REAL,
        altura_quadril REAL,
        landmarks_json TEXT,
        FOREIGN KEY(luta_id) REFERENCES lutas(id)
    );

    CREATE TABLE IF NOT EXISTS eventos_detectados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        luta_id INTEGER,
        frame_inicio INTEGER,
        tipo_golpe TEXT,
        confianca REAL,
        FOREIGN KEY(luta_id) REFERENCES lutas(id)
    );
"""