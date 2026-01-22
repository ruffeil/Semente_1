import os
from openai import OpenAI
from google import genai
from dotenv import load_dotenv

load_dotenv()

class LLMAdapter:
    def __init__(self, provider="openai"):
        self.provider = provider
        self.user_name = "Ruffeil"
        
        # Recuperação Segura das Chaves
        self.openai_key = os.getenv("LLM_API_KEY_OPENAI")
        self.gemini_key = os.getenv("LLM_API_KEY_GEMINI")

        # Validação de Segurança
        if not self.openai_key and provider == "openai":
            raise ValueError("❌ Chave OpenAI não encontrada no arquivo .env")
        if not self.gemini_key and provider == "gemini":
            raise ValueError("❌ Chave Gemini não encontrada no arquivo .env")

        # Setup Clientes
        if provider == "openai":
            self.openai_client = OpenAI(api_key=self.openai_key)
        else:
            self.gemini_client = genai.Client(api_key=self.gemini_key)

    def generate_strategic_presentation(self, data_results, branch):
        prompt = f"Aja como assistente do consultor {self.user_name}. Analise: Ramo {branch}, Dados {data_results}. Gere um reporte executivo de decisão."
        
        try:
            if self.provider == "openai":
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content
            
            elif self.provider == "gemini":
                # Sintaxe correta para google-genai 2026
                response = self.gemini_client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=prompt
                )
                return response.text
                
        except Exception as e:
            return f"⚠️ Erro no provedor {self.provider}: {e}"
