import streamlit as st
import pandas as pd
import google.generativeai as genai
from openai import OpenAI
import os

# 1. CONFIGURAÇÃO GERAL
st.set_page_config(
    page_title="SEMENTE FRAME",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CSS (ESTILO DARK MODE)
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    .stButton>button { background-color: #238636; color: white; border: none; border-radius: 6px; }
    .stButton>button:hover { background-color: #2EA043; }
    #MainMenu {visibility: hidden;} 
    footer {visibility: hidden;} 
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. MOTOR DE INTELIGÊNCIA (AGORA COM SEGREDOS)
class SementeBrain:
    def __init__(self):
        # Tenta carregar dos segredos do Streamlit
        try:
            self.openai_key = st.secrets["OPENAI_API_KEY"]
            self.gemini_key = st.secrets["GOOGLE_API_KEY"]
        except FileNotFoundError:
            st.error("❌ ERRO CRÍTICO: Chaves de API não configuradas no servidor.")
            st.stop()
        
        # Configura Gemini
        if self.gemini_key:
            try:
                genai.configure(api_key=self.gemini_key)
                self.gemini_model = genai.GenerativeModel("gemini-1.5-pro")
            except Exception as e:
                st.warning(f"Erro ao conectar Gemini: {e}")
            
        # Configura OpenAI
        if self.openai_key:
            try:
                self.openai_client = OpenAI(api_key=self.openai_key)
            except Exception as e:
                st.warning(f"Erro ao conectar OpenAI: {e}")

    def get_summary(self, df):
        return f"Linhas: {len(df)} | Colunas: {list(df.columns)} | Tipos: {df.dtypes.to_dict()}"

    def ask_gpt(self, prompt, context):
        if not hasattr(self, 'openai_client'): return "⚠️ Sistema de IA offline."
        try:
            res = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": f"Contexto: {context}. Você é o Ruffeil, Engenheiro Sênior."},
                    {"role": "user", "content": prompt}
                ]
            )
            return res.choices[0].message.content
        except Exception as e: return f"Erro no processamento: {e}"

    def get_report(self, context):
        if not hasattr(self, 'gemini_model'): return "⚠️ Módulo de Relatório offline."
        try:
            return self.gemini_model.generate_content(f"Gere um relatório técnico executivo sobre: {context}").text
        except Exception as e: return f"Erro na geração: {e}"

# 4. INTERFACE DO USUÁRIO (SIMPLIFICADA)
def main():
    with st.sidebar:
        st.title("🌱 SEMENTE FRAME")
        st.caption("Status: Conectado ao Núcleo")
        st.divider()
        # AQUI MUDOU: O usuário só vê o upload, nada de chaves.
        file = st.file_uploader("Carregar Base de Dados (CSV)", type=["csv"])
        st.info("🔒 Ambiente Seguro e Criptografado")

    if file:
        if "df" not in st.session_state:
            st.session_state.df = pd.read_csv(file)
            st.session_state.brain = SementeBrain() # O Brain pega as chaves sozinho
            st.session_state.ctx = st.session_state.brain.get_summary(st.session_state.df)
            st.session_state.msgs = [{"role": "assistant", "content": "Olá! Sou o Ruffeil. Seus dados foram processados com segurança. Como posso ajudar?"}]

        # Histórico
        for msg in st.session_state.msgs:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])

        # Chat
        if prompt := st.chat_input("Pergunte ao Semente Frame..."):
            st.session_state.msgs.append({"role": "user", "content": prompt})
            st.chat_message("user").markdown(prompt)
            
            with st.spinner("Processando..."):
                resp = st.session_state.brain.ask_gpt(prompt, st.session_state.ctx)
                st.session_state.msgs.append({"role": "assistant", "content": resp})
                st.chat_message("assistant").markdown(resp)

        # Relatório
        st.divider()
        if st.button("Gerar Relatório Técnico"):
            with st.spinner("Gerando análise executiva..."):
                rep = st.session_state.brain.get_report(st.session_state.ctx)
                with st.expander("📄 Ver Relatório Completo", expanded=True):
                    st.markdown(rep)
    else:
        st.markdown("<br><h1 style='text-align: center'>Bem-vindo ao SEMENTE FRAME 🌱</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center'>Faça o upload do CSV para iniciar a consultoria automática.</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
