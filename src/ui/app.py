import streamlit as st
import pandas as pd
import plotly.io as pio
from src.engines.predictive_engine import PredictiveEngine

# Configuração da Página com Branding SEMENTE
st.set_page_config(
    page_title="SEMENTE FRAME | Intelligence",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização de CSS para um look profissional
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #2e7d32; color: white; }
    .stChatFloatingInputContainer { bottom: 20px; }
    </style>
""", unsafe_allow_code=True)

# Header SEMENTE
st.markdown("<h1 style='color: #2e7d32;'>🌱 SEMENTE FRAME</h1>", unsafe_allow_code=True)
st.caption("A base da sua inteligência de dados | Powered by Ruffeil Architecture")

# Sidebar de Configuração (O que o usuário não precisa ver no centro)
with st.sidebar:
    st.image("https://via.placeholder.com/150x50?text=SEMENTE+AI", use_container_width=True)
    st.title("🛡️ Painel de Controle")
    
    with st.expander("🔑 Credenciais de IA", expanded=False):
        O_KEY = st.text_input("OpenAI Key", type="password", help="Usada para o chat com Ruffeil")
        G_KEY = st.text_input("Gemini Key", type="password", help="Usada para o Relatório Técnico")
    
    st.divider()
    file = st.file_uploader("📥 Ingestão de Dados (CSV)", type="csv")
    
    if st.button("🚀 Gerar Relatório SEMENTE"):
        st.session_state.generate_report = True

# Lógica Principal
if O_KEY and G_KEY and file:
    if "engine" not in st.session_state:
        st.session_state.engine = PredictiveEngine(openai_key=O_KEY, gemini_key=G_KEY)
    
    df = pd.read_csv(file)
    ctx = st.session_state.engine.process(df)

    # Espaço do Chat (O Diálogo com Ruffeil)
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Olá! Eu sou o Ruffeil. Carreguei seus dados no ecossistema Semente. Como posso te ajudar a refiná-los hoje?"}]

    for msg in st.session_state.messages:
        avatar = "🌱" if msg["role"] == "assistant" else None
        st.chat_message(msg["role"], avatar=avatar).markdown(msg["content"])

    if prompt := st.chat_input("Pergunte ao consultor..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant", avatar="🌱"):
            res = st.session_state.engine.chat_with_gpt(prompt, ctx)
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

    # Exibição do Relatório (Quando acionado)
    if st.session_state.get("generate_report"):
        st.divider()
        with st.status("Refinando Dados no Funil SEMENTE...", expanded=True):
            report = st.session_state.engine.generate_final_report(ctx)
        
        st.markdown(report)
        st.download_button("💾 Baixar Guia de Sobrevivência SEMENTE", report, "relatorio_semente.md")
        st.session_state.generate_report = False

else:
    # Tela de Boas-vindas amigável
    st.info("👋 Bem-vindo ao Semente Frame! Para começar, insira suas chaves de API e carregue um arquivo CSV na barra lateral.")
    st.image("https://via.placeholder.com/800x400?text=SEMENTE+FRAME+WORKFLOW", caption="O seu Funil de Refinamento de Dados")
