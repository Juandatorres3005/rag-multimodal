import os
from abc import ABC, abstractmethod
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# 1. Contrato base para proveedores de LLM
class LLMProvider(ABC):
    @abstractmethod
    def generate_response(self, prompt: str, context: str) -> str:
        pass

# 2. Implementación para Google Gemini API (endpoint de compatibilidad)
class GeminiProvider(LLMProvider):
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("ERROR: No se encontró GEMINI_API_KEY en las variables de entorno.")
        
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

    def generate_response(self, prompt: str, context: str) -> str:
        system_prompt = (
            "Eres un asistente técnico especializado en análisis de documentos.\n"
            "Responde a la pregunta utilizando ÚNICAMENTE el contexto proporcionado.\n"
            "Si el contexto no contiene información suficiente, indica explícitamente: "
            "'El contexto proporcionado no contiene información suficiente para responder.'\n"
            "Mantén un tono profesional, claro y directo."
        )
        full_prompt = f"Contexto:\n{context[:4000]}\n\nPregunta: {prompt}"
        
        # Lista con los modelos activos según la API de Google
        modelos_gemini = [
            "gemini-3.8-flash",
            "gemini-3.0-flash"
        ]
        
        errores = []
        for modelo in modelos_gemini:
            try:
                response = self.client.chat.completions.create(
                    model=modelo,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": full_prompt}
                    ],
                    temperature=0.1
                )
                return response.choices[0].message.content
            except Exception as e:
                errores.append(f"• {modelo}: {str(e)}")
                continue
                
        return "⚠️ Fallaron todos los modelos de Gemini:\n" + "\n".join(errores)