import streamlit as st
import pandas as pd
from src.engines.predictive_engine import PredictiveEngine

st.set_page_config(page_title="SEMENTE FRAME", layout="wide")
st.markdown("<h1 style='color: #2e7d32;'>🌱 SEMENTE FRAME</h1>", unsafe_allow_code=True)
st.caption("A base da sua inteligência de dados")

with st.sidebar:
    st.header("🛡️ Autenticação")
    O_KEY = st.text_input("OpenAI Key", type="password")
    G_KEY = st.text_input("Gemini Key", type="password")
    file = st.file_uploader("Carregar CSV", type="csv")

if O_KEY and G_KEY and file:
    if "engine" not in st.session_state:
        st.session_state.engine = PredictiveEngine(openai_key=O_KEY, gemini_key=G_KEY)
    
    df = pd.read_csv(file)
    ctx = st.session_state.engine.process(df)

    # Chat Interface
    if prompt := st.chat_input("Fale com Ruffeil..."):
        res = st.session_state.engine.chat_with_gpt(prompt, ctx)
        st.chat_message("assistant", avatar="🌱").markdown(res)

    # Relatório SEMENTE
    st.sidebar.divider()
    if st.sidebar.button("🚀 Gerar Relatório Assinado"):
        with st.spinner("Refinando relatório no estilo SEMENTE..."):
            report = st.session_state.engine.generate_final_report(ctx)
            st.markdown(report)
            st.download_button("Baixar Guia SEMENTE", report, "relatorio_semente.md")
else:
    st.info("Insira as chaves e o arquivo para ativar o ecossistema SEMENTE.")
