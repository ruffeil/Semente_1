from src.engines.base import BaseEngine
import pandas as pd

class AgroEngine(BaseEngine):
    def process(self, df: pd.DataFrame) -> dict:
        avg_ndvi = df['ndvi_index'].mean()
        avg_umidade = df['umidade_solo'].mean()
        status_safra = "Saudável" if avg_ndvi > 0.6 else "Alerta de Estresse"
        return {
            "avg_ndvi": round(avg_ndvi, 4),
            "avg_moisture": round(avg_umidade, 2),
            "crop_status": status_safra,
            "total_talhoes": len(df['id_talhao'].unique())
        }
