import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def calcular_rsi(series, periodos=14):
    """Calcula o IFR (RSI) usando a Média Móvel Exponencial."""
    delta = series.diff()
    ganho = delta.where(delta > 0, 0)
    perda = -delta.where(delta < 0, 0)

    media_ganho = ganho.ewm(com=periodos - 1, min_periods=periodos).mean()
    media_perda = perda.ewm(com=periodos - 1, min_periods=periodos).mean()

    rs = media_ganho / media_perda
    rsi = 100 - (100 / (1 + rs))
    return rsi


def criar_grafico(ticker, periodo="1y"):
    """
    Gera gráfico com Preço, Volume, RSI e PROJEÇÃO PONDERADA de 10 dias.
    """
    intervalo = "1d"

    try:
        acao = yf.Ticker(ticker)
        dados = acao.history(period=periodo, interval=intervalo)

        if dados.empty:
            return None, "Sem dados suficientes."

        # Cálculos Técnicos Básicos
        dados['MM20'] = dados['Close'].rolling(window=20).mean()
        dados['RSI'] = calcular_rsi(dados['Close'])

        # =========================================================
        # O NOVO CÉREBRO: REGRESSÃO LINEAR PONDERADA (TEMPO + VOLUME)
        # =========================================================
        texto_projecao = ""
        tamanho_janela = min(len(dados), 30)  # Analisa até os últimos 30 dias

        if tamanho_janela >= 15:
            df_recente = dados.tail(tamanho_janela).copy()
            x = np.arange(len(df_recente))
            y = df_recente['Close'].values
            vol = df_recente['Volume'].values

            # 1. PESO DO TEMPO (Decaimento Exponencial)
            # O último dia (hoje) tem peso 1.0, os dias mais antigos vão caindo para perto de 0.05
            pesos_tempo = np.exp(np.linspace(-3, 0, len(df_recente)))

            # 2. PESO DO VOLUME (Força do Movimento)
            media_vol = np.mean(vol) if np.mean(vol) > 0 else 1
            pesos_vol = vol / media_vol  # Dias com volume acima da média ganham peso > 1

            # 3. PESO FINAL COMBINADO
            pesos_finais = pesos_tempo * pesos_vol

            # Matemática: Encontra a reta, mas agora 'ouvindo' os pesos (w)
            coef = np.polyfit(x, y, 1, w=pesos_finais)
            tendencia_func = np.poly1d(coef)

            # Gerar os próximos 10 dias úteis (Pula fins de semana)
            ultima_data = df_recente.index[-1]
            datas_futuras = []
            dias_add = 1
            while len(datas_futuras) < 10:
                nova_data = ultima_data + pd.Timedelta(days=dias_add)
                if nova_data.weekday() < 5:
                    datas_futuras.append(nova_data)
                dias_add += 1

            # Valores matemáticos do futuro
            x_futuro = np.arange(len(df_recente), len(df_recente) + 10)
            y_futuro = tendencia_func(x_futuro)

            # Prepara os dados para desenhar a linha
            datas_plot = [ultima_data] + datas_futuras
            valores_plot = [y[-1]] + list(y_futuro)

            # Calcula o alvo financeiro
            preco_alvo = y_futuro[-1]
            variacao = ((preco_alvo / y[-1]) - 1) * 100

            # Identificador de Força da Projeção
            if coef[0] > 0.1:
                direcao = "FORTE ALTA"
            elif coef[0] > 0:
                direcao = "ALTA LIGEIRA"
            elif coef[0] < -0.1:
                direcao = "QUEDA BRUSCA"
            else:
                direcao = "QUEDA LIGEIRA"

            texto_projecao = f"ALVO (10 dias): R$ {preco_alvo:.2f} ({variacao:+.2f}%) | {direcao}"
        else:
            texto_projecao = "Período muito curto para gerar projeção."
            datas_plot, valores_plot, coef = [], [], [0]

        # =========================================================
        # CRIAÇÃO DO PLOT VISUAL
        # =========================================================
        fig = plt.Figure(figsize=(10, 6), dpi=100)
        gs = fig.add_gridspec(2, 1, height_ratios=[3, 1], hspace=0.1)

        # AX1: PREÇO, MÉDIA E PROJEÇÃO
        ax1 = fig.add_subplot(gs[0])
        ax1.plot(dados.index, dados['Close'],
                 label='Preço Atual', color='#3498DB', linewidth=1.5)
        ax1.plot(dados.index, dados['MM20'], label='Média Móvel (20)',
                 color='#F39C12', linestyle='--', alpha=0.8)

        # Desenhar a Projeção
        if datas_plot:
            cor_proj = '#00FF00' if coef[0] > 0 else '#FF4444'
            ax1.plot(datas_plot, valores_plot, label='Projeção Ponderada 10d',
                     color=cor_proj, linestyle='--', linewidth=2.5)

        # Volume
        fechamentos = dados['Close'].tolist()
        aberturas = dados['Open'].tolist()
        cor_vol = ['green' if c > o else 'red' for c,
                   o in zip(fechamentos, aberturas)]

        ax_vol = ax1.twinx()
        ax_vol.bar(dados.index, dados['Volume'], color=cor_vol, alpha=0.3)
        ax_vol.set_yticks([])

        ax1.set_title(f"{ticker} | Análise Técnica e Projeção ({periodo})")
        ax1.legend(loc='upper left')
        ax1.grid(True, linestyle='--', alpha=0.3)
        ax1.tick_params(axis='x', labelbottom=False)

        # AX2: RSI (IFR)
        ax2 = fig.add_subplot(gs[1], sharex=ax1)
        ax2.plot(dados.index, dados['RSI'], color='#8E44AD', label='RSI (14)')
        ax2.axhline(70, color='red', linestyle=':', alpha=0.5)
        ax2.axhline(30, color='green', linestyle=':', alpha=0.5)
        ax2.fill_between(dados.index, 70, 30, color='gray', alpha=0.1)

        ax2.set_ylabel("RSI")
        ax2.set_ylim(0, 100)
        ax2.grid(True, linestyle='--', alpha=0.3)

        fig.autofmt_xdate()

        return fig, texto_projecao

    except Exception as e:
        print(f"Erro no gráfico técnico: {e}")
        return None, f"Erro: {e}"
