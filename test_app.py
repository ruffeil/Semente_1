import pandas as pd
import json
from src.engines.predictive_engine import PredictiveEngine

try:
    print("🔍 Iniciando Teste de Integração...")
    df = pd.read_csv('datasetTreino/titanic/train.csv')
    engine = PredictiveEngine()
    result = engine.process(df)
    
    print("\n✅ SUCESSO NO PROCESSAMENTO!")
    print(f"📊 Taxa de Sobrevivência: {result['descriptive']['survival_rate']}")
    print(f"🧬 Score de Risco Calculado: {result['predictive']['risk_score']}")
    print(f"📈 Gráficos Gerados: {list(result['charts'].keys())}")
    
    with open('last_run_result.json', 'w') as f:
        json.dump(result, f, indent=4)
    print("\n📂 Resultado salvo em: last_run_result.json")
except Exception as e:
    print(f"\n❌ ERRO NO TESTE: {e}")
