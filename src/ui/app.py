import streamlit as st
import pandas as pd
import google.generativeai as genai
from openai import OpenAI
import time

# ==============================================================================
# 1. CONFIGURAÇÃO VISUAL (DARK MODE & BRANDING)
# ==============================================================================
st.set_page_config(
    page_title="SEMENTE FRAME | Data Intelligence",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Personalizado para dar o ar "SaaS Profissional"
st.markdown("""
    <style>
    /* Remover elementos padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Fundo Dark e Texto */
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #161B22; border-right: 1px solid #30363D; }
    
    /* Botões Verdes (Identidade SEMENTE) */
    .stButton>button { 
        background-color: #238636; 
        color: white; 
        border: 1px solid rgba(240,246,252,0.1); 
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.2s;
    }
    .stButton>button:hover { 
        background-color: #2EA043; 
        border-color: #8B949E;
        transform: scale(1.02);
    }
    
    /* Chat Messages */
    .stChatMessage { background-color: transparent; }
    [data-testid="stChatMessageContent"] { 
        background-color: #21262D; 
        border: 1px solid #30363D; 
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_code=True)

# ==============================================================================
# 2. MOTOR DE INTELIGÊNCIA (BACK-END EMBUTIDO)
# ==============================================================================
class SementeBrain:
    def __init__(self, openai_key, gemini_key):
        self.openai_key = openai_key
        self.gemini_key = gemini_key
        
        # Configuração Gemini
        if gemini_key:
            genai.configure(api_key=gemini_key)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-pro')
            
        # Configuração OpenAI
        if openai_key:
            self.openai_client = OpenAI(api_key=openai_key)

    def analyze_dataframe(self, df):
        """Cria um resumo técnico dos dados para dar contexto à IA"""
        buffer = []
        buffer.append(f"Total Linhas: {len(df)}")
        buffer.append(f"Colunas: {list(df.columns)}")
        buffer.append(f"Tipos de Dados: {df.dtypes.to_dict()}")
        buffer.append(f"Amostra (Head): {df.head(3).to_dict()}")
        
        # Análise de Nulos
        missing = df.isnull().sum()
        missing = missing[missing > 0]
        if not missing.empty:
            buffer.append(f"Valores Nulos: {missing.to_dict()}")
            
        return "\n".join(str(x) for x in buffer)

    def ask_ruffeil(self, question, context):
        """O Chatbot Consultivo (GPT-4o)"""
        if not self.openai_key: return "⚠️ Chave da OpenAI não configurada."
        
        prompt = f"""
        Você é o RUFFEIL, um Engenheiro de Dados Sênior e criador do framework SEMENTE.
        CONTEXTO DOS DADOS:
        {context}
        
        PERGUNTA DO USUÁRIO:
        {question}
        
        DIRETRIZES:
        1. Seja direto, técnico mas didático.
        2. Use a metodologia Semente (Ingestão -> Tratamento -> Análise).
        3. Se houver problemas nos dados (nulos, tipos errados), aponte-os.
        4. Use formatação Markdown (negrito, listas) para facilitar a leitura.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Erro na OpenAI: {str(e)}"

    def generate_report(self, context):
        """O Relatório de Refinamento (Gemini 1.5 Pro)"""
        if not self.gemini_key: return "⚠️ Chave do Gemini não configurada."
        
        prompt = f"""
        Aja como um Analista de Qualidade de Dados Sênior. Gere um RELATÓRIO TÉCNICO SEMENTE.
        
        DADOS:
        {context}
        
        ESTRUTURA DO RELATÓRIO (Use Emojis):
        1. 🎯 **Diagnóstico Inicial**: Visão geral da saúde dos dados.
        2. 🧹 **Necessidades de Limpeza**: O que precisa ser corrigido? (Nulos, Tipagem, Duplicatas).
        3. 💡 **Insights Preliminares**: O que os dados sugerem à primeira vista?
        4. 🚀 **Próximos Passos (Plano de Ação)**: 3 recomendações de engenharia.
        
        FORMATO: Markdown limpo e profissional.
        """
        
        try:
            response = self.gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ Erro no Gemini: {str(e)}"

# ==============================================================================
# 3. INTERFACE DO USUÁRIO (FRONT-END)
# ==============================================================================

# --- BARRA LATERAL ---
with st.sidebar:
    st.title("🌱 SEMENTE FRAME")
    st.caption("v1.0.0 | Ruffeil Architecture")
    st.divider()
    
    with st.expander("🔑 Configuração de Acesso", expanded=True):
        openai_api = st.text_input("OpenAI API Key", type="password")
        gemini_api = st.text_input("Gemini API Key", type="password")
        
    st.divider()
    
    uploaded_file = st.file_uploader("📂 Carregar Dataset (CSV)", type=["csv"])
    
    if uploaded_file and openai_api and gemini_api:
        st.success("Sistema Operacional")
        reset_btn = st.button("🔄 Reiniciar Análise")
        if reset_btn:
            st.session_state.messages = []
            st.rerun()
    else:
        st.warning("Aguardando Credenciais e Arquivo...")

# --- ÁREA PRINCIPAL ---
if uploaded_file and openai_api and gemini_api:
    # 1. Carregar Dados
    if 'df' not in st.session_state or reset_btn:
        st.session_state.df = pd.read_csv(uploaded_file)
        st.session_state.brain = SementeBrain(openai_api, gemini_api)
        st.session_state.context = st.session_state.brain.analyze_dataframe(st.session_state.df)
        st.session_state.messages = [{"role": "assistant", "content": "Olá! Sou o Ruffeil. Seus dados foram carregados no Semente Frame. O que deseja analisar hoje?"}]

    # 2. Exibir Chat
    st.subheader("💬 Consultoria Semente")
    
    for msg in st.session_state.messages:
        avatar = "🌱" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # 3. Input do Usuário
    if prompt := st.chat_input("Pergunte sobre seus dados..."):
        # Usuário
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
            
        # Resposta IA
        with st.chat_message("assistant", avatar="🌱"):
            with st.spinner("Analisando estrutura..."):
                response = st.session_state.brain.ask_ruffeil(prompt, st.session_state.context)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

    # 4. Área de Relatório (Expansível)
    st.divider()
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("📝 Gerar Relatório Completo"):
            with st.spinner("O Gemini está auditando os dados..."):
                report = st.session_state.brain.generate_report(st.session_state.context)
                st.session_state.report = report
    
    if 'report' in st.session_state:
        with st.expander("📄 Visualizar Relatório Técnico", expanded=True):
            st.markdown(st.session_state.report)
            st.download_button("📥 Baixar Relatório (MD)", st.session_state.report, "Relatorio_Semente.md")

else:
    # --- TELA DE BOAS VINDAS (EMPTY STATE) ---
    st.markdown("<br><br>", unsafe_allow_code=True)
    st.markdown("""
    <div style="text-align: center;">
        <h1>🌱 Bem-vindo ao SEMENTE FRAME</h1>
        <p style="font-size: 1.2em; color: #8b949e;">
            Sua plataforma de Inteligência e Refinamento de Dados.
        </p>
    </div>
    """, unsafe_allow_code=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.info("👈 Para começar, insira suas chaves de API e suba um arquivo CSV na barra lateral.")

