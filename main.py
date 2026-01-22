from src.core.orchestrator import PipelineOrchestrator
from src.engines.sales_engine import SalesEngine
from src.core.contract import SalesContract

if __name__ == "__main__":
    # Configurando o framework
    maestro = PipelineOrchestrator(
        engine=SalesEngine(), 
        schema=SalesContract, 
        branch_name="Varejo"
    )

    # Executando o Pipeline Completo
    apresentacao, arquivo = maestro.run_pipeline('test_vendas.csv')
    
    print("\n" + "="*50)
    print(apresentacao)
    print("="*50)
    print(f"\n📁 Relatório gerado com sucesso: {arquivo}")
