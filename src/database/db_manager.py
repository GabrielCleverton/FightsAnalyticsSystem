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

if __name__ == "__main__":
    db = DBMANAGER()