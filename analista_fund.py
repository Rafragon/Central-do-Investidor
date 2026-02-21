import yfinance as yf
from pydantic import BaseModel, Field, ValidationError
from typing import Optional

# Isso serve como um "molde". Se o dado do Yahoo não encaixar aqui, a gente descobre logo.


class RelatorioFundamentalista(BaseModel):
    # O 'alias' é o nome exato que vem do Yahoo Finance (API).
    # O nome da variável (esquerda) é como vamos usar no Python.
    nome: str = Field(alias="longName", default="Desconhecido")
    preco: float = Field(alias="currentPrice", default=0.0)

    # Optional[] permite que o valor seja None (nulo), comum em finanças
    pl: Optional[float] = Field(alias="trailingPE", default=None)
    dy: Optional[float] = Field(alias="dividendYield", default=None)
    roe: Optional[float] = Field(alias="returnOnEquity", default=None)

    # Dívida Líquida / EBITDA: Mede em quantos anos a empresa paga a dívida com o lucro operacional.
    # Valores acima de 3.5 são considerados arriscados.
    divida_ebitda: Optional[float] = Field(alias="debtToEbitda", default=None)

    # A lógica de colocar "%" fica presa ao dado, não solta no print
    @property
    def dy_formatado(self) -> str:
        if self.dy is not None:
            return f"{self.dy * 100:.2f}%"
        return "N/A"

    @property
    def roe_formatado(self) -> str:
        if self.roe is not None:
            return f"{self.roe * 100:.2f}%"
        return "N/A"

    @property
    def pl_formatado(self) -> str:
        if self.pl is not None:
            return f"{self.pl:.2f}"
        return "N/A"

    @property
    def divida_formatada(self) -> str:
        if self.divida_ebitda is not None:
            return f"{self.divida_ebitda:.2f}x"
        return "N/A"


def mostrar_relatorio(ticker: str):
    """
    Recebe um ticker, valida os dados com Pydantic e imprime.
    """
    print(f"\nBuscando fundamentos validados para {ticker}...")
    try:
        acao = yf.Ticker(ticker)
        dados_brutos = acao.info

        if not dados_brutos:
            print("Sem informações disponíveis na API.")
            return

        relatorio = RelatorioFundamentalista(**dados_brutos)

        print("=" * 50)
        print(f"{relatorio.nome}")
        print(f"Preço: R$ {relatorio.preco:.2f}")
        print("-" * 50)
        print(f"P/L: {relatorio.pl_formatado}")
        print(f"DY:  {relatorio.dy_formatado}")
        print(f"ROE: {relatorio.roe_formatado}")

        # Mostra o indicador de risco com um alerta visual simples
        div_str = relatorio.divida_formatada
        alerta = ""
        if relatorio.divida_ebitda and relatorio.divida_ebitda > 3.5:
            alerta = "(ALAVANCADA)"

        print(f"Dívida/EBITDA: {div_str}{alerta}")
        print("=" * 50)

    except ValidationError as e:
        print("Erro de validação dos dados!")
        for erro in e.errors():
            print(f"   -> Campo '{erro['loc'][0]}': {erro['msg']}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
