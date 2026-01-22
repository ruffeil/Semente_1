from src.engines.base import BaseEngine
import pandas as pd

class SalesEngine(BaseEngine):
    def process(self, df: pd.DataFrame) -> dict:
        # Lógica simples de exemplo: Total de Vendas
        total_vendas = (df['valor'] * df['quantidade']).sum()
        return {"total_revenue": total_vendas, "rows_processed": len(df)}
