from src.engines.base import BaseEngine
class LogisticsEngine(BaseEngine):
    def process(self, df):
        return {"total_weight": df['peso_kg'].sum(), "avg_delivery_time": df['prazo_dias'].mean()}
