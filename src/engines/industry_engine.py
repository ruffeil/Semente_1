from src.engines.base import BaseEngine
class IndustryEngine(BaseEngine):
    def process(self, df):
        status = "Manutenção Requerida" if df['temperatura'].max() > 85 else "Operação Estável"
        return {"max_temp": df['temperatura'].max(), "status": status}
