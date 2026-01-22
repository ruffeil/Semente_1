import sys
import os

# --- CORREÇÃO DO ERRO DE IMPORTAÇÃO (GPS DO PYTHON) ---
# Isso ensina o Streamlit a olhar duas pastas acima para achar o 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
# ------------------------------------------------------

import streamlit as st
import pandas as pd
from src.engines.predictive_engine import PredictiveEngine

# Configuração da Página
st.set_page_config(
    page_title="SEMENTE FRAME | Data Intelligence",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS (Design Limpo e Profissional)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #0e1117; color: #f0f2f6; }
    .stButton>button { 
        background-color: #2e7d32; 
        color: white; 
        border-radius: 8px; 
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { background-color: #4caf50; }
    </style>
""", unsafe_allow_code=True)

# Sidebar
with st.sidebar:
    st.title("🌱 Semente Frame")
    st.markdown("*Inteligência de Dados Simplificada*")
    st.divider()
    
    with st.expander("🔐 Credenciais", expanded=True):
        O_KEY = st.text_input("OpenAI Key", type="password")
        G_KEY = st.text_input("Gemini Key", type="password")

    st.divider()
    file = st.file_uploader("📂 Arraste seu CSV aqui", type="csv")
    
    if file:
        st.success("Dados prontos!")
        generate_btn = st.button("📝 Gerar Relatório Completo")
    else:
        generate_btn = False

# Área Principal
if O_KEY and G_KEY and file:
    if "engine" not in st.session_state:
        st.session_state.engine = PredictiveEngine(openai_key=O_KEY, gemini_key=G_KEY)
    
    df = pd.read_csv(file)
    ctx = st.session_state.engine.process(df)

    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role": "assistant", 
            "content": "Olá! Sou o Ruffeil. Já analisei a estrutura dos seus dados. O que você gostaria de descobrir hoje?"
        }]

    # Chat Container
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            avatar = "🌱" if msg["role"] == "assistant" else "👤"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

    # Input
    if prompt := st.chat_input("Pergunte ao consultor..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        with chat_container.chat_message("assistant", avatar="🌱"):
            with st.spinner("Ruffeil está pensando..."):
                res = st.session_state.engine.chat_with_gpt(prompt, ctx)
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

    # Relatório
    if generate_btn:
        st.divider()
        with st.status("🏗️ Construindo Guia SEMENTE...", expanded=True):
            st.write("🔍 Diagnosticando...")
            st.write("🚀 Refinando...")
            report = st.session_state.engine.generate_final_report(ctx)
        
        st.markdown(report)
        st.download_button("📥 Baixar PDF (Markdown)", report, "Guia_Semente.md")

else:
    # Tela de Boas Vindas
    st.markdown("<h1 style='text-align: center;'>Bem-vindo ao Ecossistema SEMENTE 🌱</h1>", unsafe_allow_code=True)
    st.markdown("<p style='text-align: center; color: #8b949e;'>Insira suas chaves na lateral para começar.</p>", unsafe_allow_code=True)
