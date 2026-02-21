import yfinance as yf
from servico_ia import perguntar_ao_gemini


def extrair_titulo(noticia):
    """
    Caçador de títulos blindado contra mudanças na API do Yahoo Finance.
    Verifica a estrutura nova e a antiga.
    """
    if isinstance(noticia, dict):
        # Tenta o novo formato da API (dentro de 'content')
        if 'content' in noticia and isinstance(noticia['content'], dict):
            return noticia['content'].get('title', 'Título não disponível')
        # Tenta o formato antigo
        return noticia.get('title', 'Título não disponível')
    return 'Título não formatado'


def buscar_contexto_atual(ticker):
    """
    Busca notícias recentes e pede ao Gemini para resumir.
    """
    try:
        acao = yf.Ticker(ticker)
        noticias = acao.news

        if not noticias or not isinstance(noticias, list):
            return f"Não foram encontradas notícias recentes para {ticker}."

        contexto_noticias = ""
        for n in noticias[:5]:
            titulo = extrair_titulo(n)
            contexto_noticias += f"- Título: {titulo}\n"

        prompt = f"""
        Aja como um analista de mercado financeiro.
        Com base nestas notícias recentes sobre a empresa {ticker}:
        
        {contexto_noticias}
        
        Me passe APENAS um relatório com o seguinte:
        1. Resuma em 3 pontos os temas principais.
        2. Explique brevemente como isso pode afetar o desempenho da ação no curto prazo.
        3. Dê um 'Tom de Mercado' (Ex: Otimista, Cauteloso, Pessimista).
        """

        resposta = perguntar_ao_gemini(prompt)
        return resposta

    except Exception as e:
        return f"Erro ao buscar notícias de {ticker}: {e}"


def buscar_panorama_ibovespa():
    """
    Busca notícias e dados atuais do Ibovespa para um panorama geral.
    """
    try:
        ibov = yf.Ticker("^BVSP")

        # Busca o fechamento de forma segura
        try:
            hist = ibov.history(period="2d")
        except:
            hist = []

        noticias = ibov.news
        contexto_noticias = ""

        if noticias and isinstance(noticias, list):
            for n in noticias[:5]:
                titulo = extrair_titulo(n)
                contexto_noticias += f"- {titulo}\n"
        else:
            contexto_noticias = "Sem notícias de destaque no momento."

        # Cálculo simples de variação
        if len(hist) >= 2:
            fechamento_atual = hist['Close'].iloc[-1]
            fechamento_anterior = hist['Close'].iloc[-2]
            variacao = ((fechamento_atual / fechamento_anterior) - 1) * 100
            status_mercado = f"O Ibovespa fechou em {fechamento_atual:,.0f} pontos ({variacao:+.2f}%)."
        else:
            status_mercado = "Mercado fechado ou variação indisponível."

        prompt = f"""
        Aja como um estrategista-chefe de investimentos.
        Contexto Atual do Ibovespa: {status_mercado}
        
        Notícias recentes do mercado:
        {contexto_noticias}
        
        Com base nisso, escreva um "Panorama do Dia" (máximo 150 palavras):
        1. Explique o que está movendo o índice hoje (ex: exterior, commodities, política).
        2. Qual a tendência predominante para o investidor brasileiro agora?
        3. Termine com uma frase de 'Sentimento do Mercado'.
        """

        resposta = perguntar_ao_gemini(prompt)
        return f"PANORAMA IBOVESPA\n{status_mercado}\n\n{resposta}"

    except Exception as e:
        return f"Erro crítico ao buscar panorama: {e}"
