from pydantic import BaseModel, Field
from typing import List, Optional
import json
import re
from datetime import datetime
from servico_ia import perguntar_ao_gemini


class SugestaoAcao(BaseModel):
    ticker: str = Field(description="O código da ação na B3, ex: VALE3.SA")
    nome_empresa: str = Field(description="Nome da empresa")
    setor: str = Field(description="Setor de atuação")
    risco: str = Field(description="Baixo, Médio ou Alto")
    foco_investimento: str = Field(
        description="Ex: Foco em Dividendos, Crescimento, Valorização, ou Defensivo")
    tese_investimento: str = Field(
        description="Por que comprar agora? Resumo em 1 frase.")
    preco_alvo_estimado: Optional[str] = Field(
        description="Estimativa conservadora ou 'N/A'")


class RelatorioDeOportunidades(BaseModel):
    data_analise: str
    cenario_macro: str = Field(
        description="Resumo do cenário econômico (Juros/Dólar) e Geopolítico (Guerras/Eleições/Comércio Exterior)")
    sugestoes: List[SugestaoAcao] = Field(
        description="Lista de 3 a 5 ações recomendadas")


def pesquisar_oportunidades():
    print("\nO Radar de Mercado (IA) está varrendo as oportunidades...")

    data_hoje = datetime.now().strftime("%d/%m/%Y")

    prompt = f"""
    Você é um Gestor de Carteira Sênior focado na Bolsa Brasileira (B3).
    Hoje é dia: {data_hoje}.
    
    Sua missão: Identificar oportunidades de investimento baseadas no cenário atual.
    
    1. Analise o cenário MACROECONÔMICO (Selic, Inflação, Dólar, Commodities).
    2. Analise o cenário GEOPOLÍTICO (Guerras em andamento, Tensões Comerciais EUA/China, Eleições, Cadeias de Suprimento).
    3. Selecione 4 ações da B3 que se beneficiem ou estejam protegidas neste exato cenário. Tente diversificar.
    
    SAÍDA OBRIGATÓRIA:
    Retorne APENAS um JSON válido que obedeça a seguinte estrutura, sem explicações:
    
    {{
        "data_analise": "{data_hoje}",
        "cenario_macro": "Resumo de 3 a 4 linhas interligando a macroeconomia do Brasil com o atual cenário geopolítico global...",
        "sugestoes": [
            {{
                "ticker": "XXXX.SA",
                "nome_empresa": "Nome",
                "setor": "Setor",
                "risco": "Médio",
                "foco_investimento": "Dividendos / Valorização / Crescimento / Defensiva",
                "tese_investimento": "Motivo da escolha baseada na macro e geopolítica...",
                "preco_alvo_estimado": "R$"
            }}
        ]
    }}
    """

    try:
        texto_resposta = perguntar_ao_gemini(prompt)

        texto_limpo = re.sub(r"```json|```", "", texto_resposta).strip()
        dados_dict = json.loads(texto_limpo)
        relatorio = RelatorioDeOportunidades(**dados_dict)

        return relatorio

    except json.JSONDecodeError:
        print("Erro: A IA não retornou um JSON válido.")
        print("Resposta recebida:", texto_resposta)
        return None
    except Exception as e:
        print(f"Erro ao gerar pesquisa: {e}")
        return None
