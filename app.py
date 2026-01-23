import streamlit as st
import pandas as pd
import google.generativeai as genai
from openai import OpenAI

# ==========================================================
# 1. CONFIGURAÇÃO E ESTILO (FRONT-END)
# ==========================================================
st.set_page_config(
    page_title="SEMENTE FRAME | Data Intelligence",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS Dark Mode Profissional
# CORREÇÃO: Trocamos 'unsafe_allow_code' por 'unsafe_allow_html'
st.markdown("""
    <style>
    /* Limpeza da Interface */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Cores do SEMENTE */
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    
    /* Botões Verdes */
    .stButton>button { 
        background-color: #238636; 
        color: white; 
        border: none; 
        border-radius: 6px;
        font-weight: 600;
    }
    .stButton>button:hover { background-color: #2EA043; }
    
    /* Input Chat */
    .stChatInputContainer { padding-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 2. LÓGICA DE NEGÓCIO (BACK-END EMBUTIDO)
# ==========================================================
class SementeBrain:
    def __init__(self, openai_key, gemini_key):
        self.openai_key = openai_key
        self.gemini_key = gemini_key
        
        # Inicializa APIs se as chaves existirem
        if self.gemini_key:
            genai.configure(api_key=self.gemini_key)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-pro')
        
        if self.openai_key:
            self.openai_client = OpenAI(api_key=self.openai_key)

    def get_data_summary(self, df):
        """Cria um resumo técnico do DataFrame para a IA entender"""
        buffer = []
        buffer.append(f"Linhas: {len(df)} | Colunas: {len(df.columns)}")
        buffer.append(f"Nomes das Colunas: {list(df.columns)}")
        buffer.append(f"Tipos: {df.dtypes.to_dict()}")
        
        missing = df.isnull().sum()
        if missing.sum() > 0:
            buffer.append(f"Dados Faltantes: {missing[missing > 0].to_dict()}")
            
        buffer.append(f"Amostra dos dados: {df.head(2).to_dict()}")
        return "\n".join(str(x) for x in buffer)

    def chat_ruffeil(self, prompt, context):
        """Consulta o Consultor (GPT-4o)"""
        if not self.openai_key: return "⚠️ Chave OpenAI não configurada."
        
        system_prompt = f"""
        Você é Ruffeil, Engenheiro de Dados Sênior do SEMENTE FRAME.
        Seu estilo: Direto, Técnico e Educativo.
        
        CONTEXTO DOS DADOS:
        {context}
        
        Responda à pergunta do usuário com base nesses dados.
        """
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Erro OpenAI: {e}"

    def generate_report(self, context):
        """Gera o Relatório de Refinamento (Gemini)"""
        if not self.gemini_key: return "⚠️ Chave Gemini não configurada."
        
        prompt = f"""
        Aja como um Auditor de Qualidade de Dados. Gere um relatório Markdown.
        
        DADOS:
        {context}
        
        ESTRUTURA DO RELATÓRIO:
        1. 🎯 **Diagnóstico**: O que temos aqui?
        2. 🧹 **Limpeza Necessária**: Onde estão os problemas (nulos, tipos)?
        3. 🚀 **Recomendação SEMENTE**: 3 passos para melhorar esses dados.
        """
        try:
            response = self.gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ Erro Gemini: {e}"

# ==========================================================
# 3. INTERFACE (UI)
# ==========================================================
def main():
    # --- SIDEBAR ---
    with st.sidebar:
        st.title("🌱 SEMENTE FRAME")
        st.markdown("v1.0.0 | Monolito")
        st.divider()
        
        with st.expander("🔐 Acesso", expanded=True):
            openai_key = st.text_input("OpenAI Key", type="password")
            gemini_key = st.text_input("Gemini Key", type="password")
            
        uploaded_file = st.file_uploader("📂 Carregar CSV", type=["csv"])

    # --- MAIN AREA ---
    if uploaded_file and openai_key and gemini_key:
        # Carregar ou Recuperar Estado
        if "df" not in st.session_state:
            st.session_state.df = pd.read_csv(uploaded_file)
            st.session_state.brain = SementeBrain(openai_key, gemini_key)
            st.session_state.context = st.session_state.brain.get_data_summary(st.session_state.df)
            st.session_state.messages = [{"role": "assistant", "content": "Olá! Sou o Ruffeil. Dados carregados. Como posso ajudar?"}]

        # Exibir Chat
        st.subheader("💬 Consultoria Semente")
        for msg in st.session_state.messages:
            avatar = "🌱" if msg["role"] == "assistant" else "👤"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

        # Input do Usuário
        if prompt := st.chat_input("Pergunte sobre os dados..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)
            
            with st.chat_message("assistant", avatar="🌱"):
                with st.spinner("Analisando..."):
                    resp = st.session_state.brain.chat_ruffeil(prompt, st.session_state.context)
                    st.markdown(resp)
                    st.session_state.messages.append({"role": "assistant", "content": resp})

        # Área de Relatório
        st.divider()
        if st.button("📝 Gerar Relatório Técnico Completo"):
            with st.spinner("Gemini auditando dados..."):
                report = st.session_state.brain.generate_report(st.session_state.context)
            
            with st.expander("📄 Visualizar Relatório", expanded=True):
                st.markdown(report)

    else:
        # Tela Inicial
        st.markdown("<br><h1 style='text-align: center'>Bem-vindo ao SEMENTE FRAME 🌱</h1>", unsafe_allow_code=True)
        st.info("👈 Insira suas chaves e suba um CSV para começar.")

if __name__ == "__main__":
    main()
