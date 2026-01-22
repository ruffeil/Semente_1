from src.engines.base import BaseEngine
import pandas as pd
import google.generativeai as genai
from openai import OpenAI
import os

class PredictiveEngine(BaseEngine):
    def __init__(self, openai_key=None, gemini_key=None):
        self.openai_client = OpenAI(api_key=openai_key) if openai_key else None
        if gemini_key:
            genai.configure(api_key=gemini_key)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-pro')

    def chat_with_gpt(self, user_input, context_data):
        prompt = f"""
        Você é Ruffeil, um consultor sênior de dados do ecossistema SEMENTE.
        Sua personalidade é: Acolhedora, Didática e Clara.
        Explique os dados sem 'tiopês' técnico excessivo.
        Dados: {context_data}
        Pergunta: {user_input}
        """
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    def generate_final_report(self, context_data):
        prompt = f"""
        Crie um 'Guia de Sobrevivência' sobre estes dados: {context_data}.
        Assinatura: "GERADO POR SEMENTE FRAME".
        Estilo: Funil de Refinamento (Diagnóstico -> Ação -> Resultado).
        Use emojis e bullet points.
        """
        response = self.gemini_model.generate_content(prompt)
        return response.text

    def process(self, df: pd.DataFrame) -> dict:
        df = df.copy()
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        missing = df.isnull().sum().to_dict()
        return {
            "resumo": {
                "total_linhas": len(df),
                "colunas": list(df.columns),
                "dados_faltantes": {k:v for k,v in missing.items() if v > 0},
                "colunas_numericas": numeric_cols
            },
            "amostra_head": df.head(3).to_dict()
        }
