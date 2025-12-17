import sqlite3
import os
from src.database.schema import INSTRUCOES_CRIACAO

class DBMANAGER:
    def __init__(self, db_path=None):
        if db_path == None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            db_path = os.path.join(project_root, 'data','fight_data.db')
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        try:
            self.cursor.executescript(INSTRUCOES_CRIACAO)
            self.conn.commit()
            print(f"Banco de dados conectado com sucesso: {self.db_path}")
        except sqlite3.Error as e:
            print(f"Erro ao criar as tabelas: {e}")


    def iniciar_luta(self, nome_video):
        query = "INSERT INTO lutas(video_nome) VALUES(?)"
        self.cursor.execute(query, (nome_video,))
        self.conn.commit()
        return self.cursor.lastrowid

    def salvar_frame(self, luta_id, frame_num, person_id, ang_dir, ang_esq, alt_quadril, json_dump):
        query = """
                INSERT INTO raw_data 
                (luta_id, frame_numero, person_id, angulo_cotovelo_dir, angulo_cotovelo_esq, altura_quadril, landmarks_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
        self.cursor.execute(query, (luta_id, frame_num, person_id, ang_dir, ang_esq, alt_quadril, json_dump))
        self.conn.commit()

if __name__ == "__main__":
    db = DBMANAGER()