import streamlit as st
import pandas as pd
import plotly.io as pio
from src.engines.predictive_engine import PredictiveEngine

# Configuração de Identidade Visual
st.set_page_config(page_title="SEMENTE FRAME | Intelligence", page_icon="🌱", layout="centered")

# CSS para esconder o menu padrão e customizar cores
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    .stButton>button { 
        background-color: #2e7d32; 
        color: white; 
        border-radius: 20px; 
        border: none;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #4caf50; border: none; }
    .css-1d391kg { background-color: #161b22; } 
    </style>
""", unsafe_allow_code=True)

# Header Minimalista
st.markdown("<h1 style='text-align: center; color: #4caf50;'>🌱 SEMENTE FRAME</h1>", unsafe_allow_code=True)
st.markdown("<p style='text-align: center; color: #8b949e;'>A base da sua inteligência de dados.</p>", unsafe_allow_code=True)

# Sidebar Ultra-Limpa
with st.sidebar:
    st.markdown("### 🔐 Acesso")
    O_KEY = st.text_input("OpenAI Key", type="password")
    G_KEY = st.text_input("Gemini Key", type="password")
    st.divider()
    st.markdown("### 📥 Ingestão")
    file = st.file_uploader("Suba seu arquivo CSV", type="csv", label_visibility="collapsed")
    st.divider()
    generate_btn = st.button("🚀 GERAR GUIA SEMENTE")

# Área Principal: Diálogo com Ruffeil
if O_KEY and G_KEY and file:
    if "engine" not in st.session_state:
        st.session_state.engine = PredictiveEngine(openai_key=O_KEY, gemini_key=G_KEY)
    
    df = pd.read_csv(file)
    ctx = st.session_state.engine.process(df)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Chat estilizado
    chat_placeholder = st.container()
    with chat_placeholder:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"], avatar="🌱" if msg["role"]=="assistant" else None):
                st.markdown(msg["content"])

    if prompt := st.chat_input("Fale com Ruffeil sobre este dataset..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_placeholder.chat_message("user"): st.markdown(prompt)
        
        with chat_placeholder.chat_message("assistant", avatar="🌱"):
            res = st.session_state.engine.chat_with_gpt(prompt, ctx)
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

    # Trigger do Relatório (Estilo Funil dos seus PDFs)
    if generate_btn:
        st.divider()
        with st.status("🛠️ Aplicando Funil de Refinamento SEMENTE...", expanded=True):
            report = st.session_state.engine.generate_final_report(ctx)
            st.write("✅ Diagnóstico Concluído")
            st.write("✅ Dados Padronizados")
            st.write("✅ Relatório SEMENTE Assinado")
        
        st.markdown(report)
        st.download_button("📂 BAIXAR RELATÓRIO PDF (Markdown)", report, "guia_semente.md")

else:
    st.markdown("""
        <div style='text-align: center; padding: 50px;'>
            <h3 style='color: #8b949e;'>Aguardando chaves e dados para iniciar...</h3>
            <p>Insira suas credenciais na barra lateral para ativar o ecossistema.</p>
        </div>
    """, unsafe_allow_code=True)
