import streamlit as st
import pandas as pd
import json
import plotly.io as pio
from src.core.orchestrator import PipelineOrchestrator
from src.engines.sales_engine import SalesEngine
from src.engines.agro_engine import AgroEngine
from src.engines.predictive_engine import PredictiveEngine
from src.core.contract import (
    SalesContract, AgroContract, TitanicContract
)

st.set_page_config(page_title="SEMENTE_FRAME Suite", page_icon="🌱", layout="wide")

st.title("🌱 SEMENTE_FRAME | Intelligence Suite")
st.markdown("---")

# Sidebar - Navegação
st.sidebar.header("Painel de Controle")
tab_selection = st.sidebar.radio("Navegar para:", ["Dashboard", "Nova Análise", "Histórico"])

if tab_selection == "Nova Análise":
    ramo = st.sidebar.selectbox("Selecione o Ramo", ["Titanic", "Agro", "Varejo"])
    
    mapping = {
        "Varejo": (SalesEngine(), SalesContract),
        "Agro": (AgroEngine(), AgroContract),
        "Titanic": (PredictiveEngine(), TitanicContract)
    }
    
    engine, schema = mapping[ramo]
    
    uploaded_file = st.file_uploader("Suba seu arquivo (CSV)", type=["csv"])
    
    if uploaded_file:
        if st.button("Executar Inteligência 360°"):
            with st.spinner("SEMENTE_FRAME: Validando, Limpando e Analisando..."):
                # Salvando temp
                temp_path = f"temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f: f.write(uploaded_file.getbuffer())
                
                # Orquestração
                maestro = PipelineOrchestrator(engine, schema, ramo)
                apresentacao, report_path = maestro.run_pipeline(temp_path)
                
                # Exibição
                st.success("Processamento concluído!")
                
                c1, c2 = st.columns([1, 1])
                
                with c1:
                    st.subheader("🤖 Análise Estratégica (IA)")
                    st.markdown(apresentacao)
                
                with c2:
                    st.subheader("📊 Visualizações de BI")
                    # Recuperando dados do banco para gráficos (via engine output)
                    # No MVP, vamos usar dados direto da engine processada
                    res = engine.process(pd.read_csv(temp_path))
                    if 'charts' in res:
                        st.plotly_chart(pio.from_json(res['charts']['class_chart']), use_container_width=True)
                        st.plotly_chart(pio.from_json(res['charts']['sex_chart']), use_container_width=True)

elif tab_selection == "Dashboard":
    st.subheader("📈 Visão Consolidada do Core")
    # Aqui chamamos a lógica do dashboard_preview que criamos antes
    import sqlite3
    conn = sqlite3.connect('semente_frame.db')
    df_logs = pd.read_sql_query("SELECT * FROM tb_ingestion_logs", conn)
    st.dataframe(df_logs, use_container_width=True)
    st.metric("Total de Ingestões", len(df_logs))
    conn.close()

