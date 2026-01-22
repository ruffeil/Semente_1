import sqlite3
import pandas as pd
import json

def get_dashboard_data():
    conn = sqlite3.connect('semente_frame.db')
    
    # Query unindo Ingestão (Bronze) com Insights (Gold)
    query = """
    SELECT 
        l.nm_arquivo_origem as Arquivo,
        l.dt_upload as Data,
        g.js_metricas_tecnicas as Metricas
    FROM tb_ingestion_logs l
    JOIN tb_gold_insights g ON l.id_log = g.id_log
    ORDER BY l.dt_upload DESC
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Formatando o JSON para colunas legíveis
    if not df.empty:
        # Extrai os dados do JSON salvo no banco
        df['Resultado'] = df['Metricas'].apply(lambda x: json.loads(x).get('status', 'N/A') if 'status' in x else 'Processado')
        df['Resumo_IA'] = df['Metricas'].apply(lambda x: json.loads(x).get('narrative', '')[:80] + "...")
        
        return df[['Data', 'Arquivo', 'Resultado', 'Resumo_IA']]
    return "Nenhum dado encontrado."

if __name__ == "__main__":
    print("\n" + "="*30)
    print("      SEMENTE_FRAME DASHBOARD      ")
    print("="*30 + "\n")
    
    print(get_dashboard_data().to_string(index=False))
    print("\n" + "="*80)
    print("Dica: Os relatórios detalhados estão na pasta /reports")
