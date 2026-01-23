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

# 3. MOTOR DE INTELIGÊNCIA
class SementeBrain:
    def __init__(self):
        try:
            self.openai_key = st.secrets["OPENAI_API_KEY"]
            self.gemini_key = st.secrets["GOOGLE_API_KEY"]
        except Exception:
            st.error("❌ Erro: Chaves de API não configuradas corretamente.")
            st.stop()
        
        # Configura Gemini (Ajustado para 1.5-flash para maior compatibilidade)
        if self.gemini_key:
            try:
                genai.configure(api_key=self.gemini_key)
                # Mudança estratégica de modelo aqui para evitar o Erro 404
                self.gemini_model = genai.GenerativeModel("gemini-1.5-flash")
            except Exception as e:
                st.warning(f"Erro na conexão Gemini: {e}")
            
        # Configura OpenAI
        if self.openai_key:
            try:
                self.openai_client = OpenAI(api_key=self.openai_key)
            except Exception as e:
                st.warning(f"Erro na conexão OpenAI: {e}")

    def get_summary(self, df):
        return f"Linhas: {len(df)} | Colunas: {list(df.columns)} | Tipos: {df.dtypes.to_dict()}"

    def ask_gpt(self, prompt, context):
        if not hasattr(self, 'openai_client'): return "⚠️ Módulo de IA indisponível."
        try:
            res = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": f"Contexto: {context}. Você é a Semente do Conhecimento, especialista em engenharia de dados."},
                    {"role": "user", "content": prompt}
                ]
            )
            return res.choices[0].message.content
        except Exception as e: return f"Erro no chat: {e}"

    def get_report(self, context):
        if not hasattr(self, 'gemini_model'): return "⚠️ Módulo de relatório indisponível."
        try:
            # Prompt focado em análise técnica
            prompt = f"Aja como a Semente do Conhecimento. Gere um relatório técnico detalhado sobre estes dados: {context}. Estruture com Diagnóstico, Limpeza e Recomendações."
            response = self.gemini_model.generate_content(prompt)
            return response.text
        except Exception as e: 
            return f"❌ Erro na geração do relatório: {e}. Tente novamente em instantes."

# 4. INTERFACE
def main():
    with st.sidebar:
        st.title("🌱 SEMENTE FRAME")
        st.caption("v1.2.0 | Semente do Conhecimento")
        st.divider()
        file = st.file_uploader("Carregar Base de Dados (CSV)", type=["csv"])
        st.info("🔒 Conexão Segura Ativa")

    if file:
        if "df" not in st.session_state:
            st.session_state.df = pd.read_csv(file)
            st.session_state.brain = SementeBrain()
            st.session_state.ctx = st.session_state.brain.get_data_summary(st.session_state.df)
            st.session_state.msgs = [{"role": "assistant", "content": "Olá! Sou a Semente do Conhecimento. Seus dados estão prontos. O que vamos descobrir hoje?"}]

        for msg in st.session_state.msgs:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])

        if prompt := st.chat_input("Pergunte à Semente do Conhecimento..."):
            st.session_state.msgs.append({"role": "user", "content": prompt})
            st.chat_message("user").markdown(prompt)
            with st.spinner("Analisando..."):
                resp = st.session_state.brain.ask_gpt(prompt, st.session_state.ctx)
                st.session_state.msgs.append({"role": "assistant", "content": resp})
                st.chat_message("assistant").markdown(resp)

        st.divider()
        if st.button("📝 Gerar Relatório Técnico"):
            with st.spinner("Semente do Conhecimento auditando dados..."):
                rep = st.session_state.brain.get_report(st.session_state.ctx)
                st.markdown(rep)
    else:
        st.markdown("<br><h1 style='text-align: center'>Bem-vindo ao SEMENTE FRAME 🌱</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center'>Suba um arquivo CSV para iniciar a consultoria automática.</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
