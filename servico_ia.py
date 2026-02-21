import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
CHAVE_API = os.getenv("GOOGLE_API_KEY")

if CHAVE_API:
    genai.configure(api_key=CHAVE_API)


def perguntar_ao_gemini(prompt, temperatura=0.4):
    """
    Função centralizada para chamadas de API.
    Pode ser usada por qualquer outro módulo do projeto.
    """
    try:
        # Você pode centralizar a escolha do modelo aqui
        model = genai.GenerativeModel('gemini-2.5-flash')

        response = model.generate_content(
            prompt,
            generation_config={"temperature": temperatura}
        )

        return response.text
    except Exception as e:
        return f"Erro na comunicação com a IA: {e}"
