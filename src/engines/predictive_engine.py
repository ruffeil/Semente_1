from src.engines.base import BaseEngine
import pandas as pd
import google.generativeai as genai
from openai import OpenAI

class PredictiveEngine(BaseEngine):
    def __init__(self, openai_key=None, gemini_key=None):
        self.openai_client = OpenAI(api_key=openai_key) if openai_key else None
        if gemini_key:
            genai.configure(api_key=gemini_key)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-pro')

    def chat_with_gpt(self, user_input, context_data):
        prompt = f"Você é Ruffeil, o rosto da SEMENTE. Use estes dados {context_data} para responder: {user_input}. Mantenha o tom de consultor sênior."
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    def generate_final_report(self, context_data):
        prompt = f"""
        Você é o Designer Chefe da SEMENTE. Crie um relatório sobre {context_data} com estas diretrizes baseadas no 'Funil de Refinamento SEMENTE':
        
        1. ASSINATURA: O documento deve começar e terminar com: "GERADO POR SEMENTE FRAME".
        2. ESTRUTURA: Divida em: Ingestão, Diagnóstico, Limpeza, Padronização e Refinamento (Saída).
        3. DICIONÁRIO VISUAL: Tabela comparando Atributos do Dado vs Valor de Negócio.
        4. CHECKLIST ANTI-ERRO: Liste 3 pontos de atenção para evitar falhas na análise.
        5. CALL TO ACTION: No final, convide para o SaaS em semente-frame.ai.
        
        Use Markdown rico com emojis e divisores.
        """
        response = self.gemini_model.generate_content(prompt)
        return response.text

    def process(self, df: pd.DataFrame) -> dict:
        df = df.copy()
        df['Age'] = df['Age'].fillna(df['Age'].mean())
        return {
            "metrics": {
                "sobrevivencia": f"{round(df['Survived'].mean()*100, 2)}%",
                "pax_total": len(df)
            }
        }
