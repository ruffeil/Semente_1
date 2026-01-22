import pandas as pd
from src.utils.cleaning import DataSanitizer
from src.utils.security import SecurityManager
from src.utils.logger import setup_semente_logger
from src.core.contract import DataValidator
from src.adapters.database import DatabaseAdapter
from src.adapters.llm_adapter import LLMAdapter
from src.adapters.exporter import DataExporter

class PipelineOrchestrator:
    def __init__(self, engine, schema, branch_name):
        self.engine = engine
        self.schema = schema
        self.branch_name = branch_name
        self.db = DatabaseAdapter()
        self.llm = LLMAdapter(provider="openai") # Ou gemini
        self.logger = setup_semente_logger()

    def run_pipeline(self, raw_data_path: str):
        self.logger.info(f"Iniciando Atendimento para {self.branch_name}")
        
        # 1. Ingestão e Log Bronze
        log_id = self.db.log_ingestion(raw_data_path)
        df = pd.read_csv(raw_data_path)
        
        # 2. Validação de Contrato
        try:
            DataValidator.validate_schema(df, self.schema)
            self.logger.info("Contrato validado.")
        except Exception as e:
            self.logger.error(f"Falha no contrato: {e}")
            return f"❌ Erro: {e}"

        # 3. Segurança (LGPD) - Mascarando IDs de Produto (Exemplo)
        df = SecurityManager.mask_pii(df, ['id_produto'])

        # 4. Higienização Silver
        df_clean = DataSanitizer.clean(df)

        # 5-7. Processamento Gold
        results = self.engine.process(df_clean)
        
        # 8. IA e Exportação
        presentation = self.llm.generate_strategic_presentation(results, self.branch_name)
        report_path = DataExporter.save_to_markdown(presentation, self.branch_name)
        
        # Persistência
        results['narrative'] = presentation
        self.db.save_gold_insights(log_id, results)
        
        self.logger.info(f"Pipeline finalizado. Relatório em {report_path}")
        return presentation, report_path
