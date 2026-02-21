import yfinance as yf
import pandas as pd
from analista_fund import RelatorioFundamentalista
import gerenciador_carteira


def buscar_melhores_oportunidades():
    """
    O Agente varre a carteira procurando:
    1. Preço Justo (P/L)
    2. Rentabilidade (ROE)
    3. SEGURANÇA (Dívida Controlada)
    """
    resultados = []
    tickers_alvo = gerenciador_carteira.carregar_carteira()

    if not tickers_alvo:
        return pd.DataFrame(columns=["Ticker", "Preço", "P/L", "ROE", "Dívida/EBITDA"])

    print(
        f"Agente: Analisando risco e retorno de {len(tickers_alvo)} ativos...")

    for ticker in tickers_alvo:
        try:
            acao = yf.Ticker(ticker)
            dados = RelatorioFundamentalista(**acao.info)

            passou_no_filtro = False

            # Regra 1: P/L positivo e aceitável (não muito caro)
            condicao_pl = (dados.pl is not None and 0 < dados.pl < 20)

            # Regra 2: ROE decente (acima de 8% - ajustado para ser realista)
            condicao_roe = (dados.roe is not None and dados.roe > 0.08)

            # Regra 3: Dívida Saudável (Abaixo de 3.5x EBITDA)
            # Se o dado não existir (None), assumimos risco e pulamos (ou aceitamos com cautela)
            # Aqui vou ser conservador: tem que ter o dado e ser baixo.
            condicao_divida = (
                dados.divida_ebitda is not None and dados.divida_ebitda < 3.5)

            if condicao_pl and condicao_roe and condicao_divida:
                passou_no_filtro = True

            if passou_no_filtro:
                resultados.append({
                    "Ticker": ticker,
                    "Preço": dados.preco,
                    "P/L": dados.pl,
                    "ROE": dados.roe,
                    "Dívida/EBITDA": dados.divida_ebitda
                })

        except Exception:
            continue

    df = pd.DataFrame(resultados)

    if not df.empty:
        df = df.sort_values(by="ROE", ascending=False)
        return df
    else:
        return pd.DataFrame()
