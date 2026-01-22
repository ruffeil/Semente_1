from src.engines.base import BaseEngine
class HealthEngine(BaseEngine):
    def process(self, df):
        risco = "Elevado" if df['pressao_sistolica'].mean() > 140 else "Normal"
        return {"avg_age": df['idade'].mean(), "risk_level": risco}
