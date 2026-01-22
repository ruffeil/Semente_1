import sqlite3 # Usando SQLite para o MVP local, facilmente migrável para PostgreSQL/Azure
import json
from datetime import datetime

class DatabaseAdapter:
    def __init__(self, db_path="semente_frame.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Inicializa as tabelas se não existirem (Baseado no SQL planeado)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Simplificação do schema para o MVP local
            cursor.execute('''CREATE TABLE IF NOT EXISTS tb_ingestion_logs 
                (id_log INTEGER PRIMARY KEY AUTOINCREMENT, nm_arquivo_origem TEXT, dt_upload TIMESTAMP)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS tb_gold_insights 
                (id_insight INTEGER PRIMARY KEY AUTOINCREMENT, id_log INTEGER, js_metricas_tecnicas TEXT)''')
            conn.commit()

    def log_ingestion(self, filename):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tb_ingestion_logs (nm_arquivo_origem, dt_upload) VALUES (?, ?)", 
                           (filename, datetime.now()))
            return cursor.lastrowid

    def save_gold_insights(self, log_id, metrics):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tb_gold_insights (id_log, js_metricas_tecnicas) VALUES (?, ?)", 
                           (log_id, json.dumps(metrics)))
            conn.commit()
