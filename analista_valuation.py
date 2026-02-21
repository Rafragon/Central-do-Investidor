import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


def gerar_analise_valuation(ticker):
    """
    Retorna uma tupla: (texto_relatorio, objeto_figura_grafico)
    """
    try:
        acao = yf.Ticker(ticker)
        info = acao.info

        preco_atual = info.get('currentPrice', 0)
        if preco_atual == 0:
            return f"Erro: Preço atual não encontrado para {ticker}.", None

        relatorio = f"ANÁLISE DE VALUATION E DIVIDENDOS: {ticker}\n"
        relatorio += "="*50 + "\n"

        # ==========================================
        # 1. VALUATION: FÓRMULA DE GRAHAM
        # ==========================================
        # Preço Justo = Raiz Quadrada de (22.5 * LPA * VPA)
        lpa = info.get('trailingEps', 0)  # Lucro por Ação
        vpa = info.get('bookValue', 0)    # Valor Patrimonial por Ação

        relatorio += "⚖️ VALUATION (Preço Justo de Graham)\n"

        if lpa > 0 and vpa > 0:
            preco_justo = np.sqrt(22.5 * lpa * vpa)
            margem_seguranca = (
                (preco_justo - preco_atual) / preco_justo) * 100

            relatorio += f"Preço Atual: R$ {preco_atual:.2f}\n"
            relatorio += f"Preço Justo Estimado: R$ {preco_justo:.2f}\n"

            if margem_seguranca > 0:
                relatorio += f"Margem de Segurança: {margem_seguranca:.2f}% (Ação está BARATA)\n"
            else:
                relatorio += f"Margem de Segurança: {margem_seguranca:.2f}% (Ação está CARA)\n"
        else:
            relatorio += f"Preço Atual: R$ {preco_atual:.2f}\n"
            relatorio += "Fórmula de Graham inválida: A empresa possui Lucro ou Patrimônio negativo.\n"

        relatorio += "-"*50 + "\n"

        # ==========================================
        # 2. ANÁLISE DE DIVIDENDOS E HISTÓRICO
        # ==========================================
        historico_div = acao.dividends

        fig = None  # Variável para o gráfico

        if historico_div is not None and not historico_div.empty:
            # Agrupar dividendos por ano
            div_por_ano = historico_div.groupby(historico_div.index.year).sum()

            # Pegar apenas os últimos 5 anos completos
            ano_atual = datetime.now().year
            ultimos_5_anos = div_por_ano[div_por_ano.index >= (ano_atual - 5)]

            relatorio += "HISTÓRICO DE DIVIDENDOS (Últimos 5 anos)\n"
            if not ultimos_5_anos.empty:
                media_anual = ultimos_5_anos.mean()
                dy_projetado = (media_anual / preco_atual) * 100

                for ano, valor in ultimos_5_anos.items():
                    relatorio += f"{ano}: R$ {valor:.2f} por ação\n"

                relatorio += f"\nMédia Anual: R$ {media_anual:.2f}\n"
                relatorio += f"Projeção de DY p/ Próximo Ano (Base Histórica): {dy_projetado:.2f}%\n"

                # --- CRIAR GRÁFICO DE BARRAS DE DIVIDENDOS ---
                plt.style.use('dark_background')
                fig = plt.Figure(figsize=(8, 4), dpi=100)
                ax = fig.add_subplot(111)

                # Barras laranjas para combinar com o seu design
                ax.bar(ultimos_5_anos.index.astype(str),
                       ultimos_5_anos.values, color='#FF6B00', alpha=0.8)
                ax.set_title(
                    f"Evolução de Dividendos Pagos - {ticker}", fontweight='bold')
                ax.set_ylabel("Valor por Ação (R$)")

                # Adicionar o valor em cima de cada barra
                for i, v in enumerate(ultimos_5_anos.values):
                    ax.text(
                        i, v + 0.05, f"R$ {v:.2f}", ha='center', color='white', fontweight='bold')

                ax.grid(axis='y', linestyle='--', alpha=0.3)

            else:
                relatorio += "A empresa não pagou dividendos consistentes recentemente.\n"
        else:
            relatorio += "💰 DIVIDENDOS\nNenhum histórico de dividendos encontrado.\n"

        relatorio += "="*50 + "\n"

        return relatorio, fig

    except Exception as e:
        return f"Erro ao calcular valuation para {ticker}: {e}", None
