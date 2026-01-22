from src.core.orchestrator import PipelineOrchestrator
from src.engines.sales_engine import SalesEngine
from src.engines.agro_engine import AgroEngine
from src.engines.health_engine import HealthEngine
from src.engines.logistics_engine import LogisticsEngine
from src.engines.industry_engine import IndustryEngine
from src.core.contract import SalesContract, AgroContract, HealthContract, LogisticsContract, IndustryContract

test_suites = [
    ("Varejo", SalesEngine(), SalesContract, 'test_vendas.csv'),
    ("Agro", AgroEngine(), AgroContract, 'test_agro.csv'),
    ("Saude", HealthEngine(), HealthContract, 'test_health.csv'),
    ("Logistica", LogisticsEngine(), LogisticsContract, 'test_logistics.csv'),
    ("Industria", IndustryEngine(), IndustryContract, 'test_industry.csv')
]

for name, engine, schema, csv_file in test_suites:
    print(f"\n🚀 TESTANDO RAMO: {name.upper()}")
    maestro = PipelineOrchestrator(engine, schema, name)
    try:
        apresentacao, arquivo = maestro.run_pipeline(csv_file)
        print(f"✅ Sucesso! Relatório gerado: {arquivo}")
    except Exception as e:
        print(f"❌ Falha no Ramo {name}: {e}")

print("\n🎯 TODOS OS RAMOS FORAM PROCESSADOS PELO CORE SEMENTE_FRAME.")
