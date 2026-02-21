import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from servico_ia import perguntar_ao_gemini


def realizar_batalha(tickers):
    """
    Recebe uma lista de tickers (ex: ['PETR4.SA', 'VALE3.SA']).
    Retorna uma tupla: (texto_relatorio, objeto_figura_grafico)
    """
    relatorio_texto = ""  # Variável para acumular o texto

    msg_inicial = f"⚔️ PREPARANDO A ARENA PARA: {', '.join(tickers)}...\n"
    print(msg_inicial)
    relatorio_texto += msg_inicial + "\n"

    # --- 1. DOWNLOAD DOS DADOS ---
    try:
        # Baixa tudo de uma vez
        dados = yf.download(tickers, period="1y", progress=False)['Close']

        # Se for apenas 1 ticker, o pandas retorna Series, precisamos de DataFrame
        if isinstance(dados, pd.Series):
            dados = dados.to_frame()

        # Remove dias vazios
        dados.dropna(inplace=True)

        if dados.empty:
            erro_msg = "Erro: Não consegui baixar dados suficientes para comparar."
            return erro_msg, None

    except Exception as e:
        return f"Erro crítico no download: {e}", None

    # --- 2. TABELA DE FUNDAMENTOS (LADO A LADO) ---
    tabela_header = "\nCOMPARATIVO FUNDAMENTALISTA:\n" + ("-" * 65) + "\n"
    header_cols = f"{'INDICADOR':<15} |"
    for t in tickers:
        header_cols += f" {t.replace('.SA', ''):<10} |"

    relatorio_texto += tabela_header + header_cols + "\n" + ("-" * 65) + "\n"

    # Dicionário para guardar infos pra IA
    infos_ia = {}

    try:
        indicadores = ['currentPrice', 'trailingPE',
                       'dividendYield', 'returnOnEquity', 'sector']
        nomes_ind = ['Preço (R$)', 'P/L (anos)', 'Div. Yield', 'ROE', 'Setor']

        dados_fund = {}
        # Coleta dados (com proteção se o ticker falhar)
        for t in tickers:
            try:
                info = yf.Ticker(t).info
                dados_fund[t] = info
                infos_ia[t] = info
            except:
                dados_fund[t] = {}
                infos_ia[t] = {}

        # Monta as linhas da tabela
        for i, ind_key in enumerate(indicadores):
            linha = f"{nomes_ind[i]:<15} |"

            for t in tickers:
                valor = dados_fund[t].get(ind_key, 'N/A')

                # Formatações
                if isinstance(valor, (int, float)):
                    if ind_key in ['dividendYield', 'returnOnEquity']:
                        valor = f"{valor*100:.2f}%"
                    elif ind_key == 'currentPrice':
                        valor = f"{valor:.2f}"
                    elif ind_key == 'trailingPE':
                        valor = f"{valor:.1f}"

                linha += f" {str(valor):<10} |"
            relatorio_texto += linha + "\n"

    except Exception as e:
        relatorio_texto += f"\nErro ao montar tabela detalhada: {e}\n"

    relatorio_texto += ("-" * 65) + "\n"

    # --- 3. ANÁLISE DO JUIZ (IA) ---
    relatorio_texto += "\nINVOCANDO O JUIZ ...\n"

    try:
        prompt = f"""
        Aja como um juiz de batalha de investimentos agressivo e direto.
        Data: {datetime.now().strftime('%d/%m/%Y')}
        Competidores: {', '.join(tickers)}
        
        DADOS TÉCNICOS:
        """

        for t in tickers:
            info = infos_ia.get(t, {})
            nome = info.get('shortName', t)
            pl = info.get('trailingPE', 'N/A')
            dy = info.get('dividendYield', 0)
            roe = info.get('returnOnEquity', 0)
            setor = info.get('sector', 'N/A')
            prompt += f"\n- {t} ({nome}): Setor {setor} | P/L: {pl} | DY: {dy} | ROE: {roe}"

        prompt += """
        
        Com base APENAS nestes números:
        1. Quem vence nos FUNDAMENTOS (Solidez)?
        2. Quem vence nos DIVIDENDOS (Renda)?
        3. VEREDITO FINAL: Qual a melhor escolha HOJE?
        
        Seja breve (máximo 5 linhas). Sem enrolação.
        """

        # Ajustado para o modelo correto
        resposta = perguntar_ao_gemini(prompt)

        relatorio_texto += "\n" + "="*60 + "\n"
        relatorio_texto += resposta
        relatorio_texto += "\n" + "="*60 + "\n"

    except Exception as e:
        relatorio_texto += f"\nO Juiz IA não pôde comparecer: {e}\n"

    # --- 4. BATALHA GRÁFICA (NORMALIZADA) ---
    # Normalização: (Preço / Preço Inicial) * 100
    dados_normalizados = (dados / dados.iloc[0]) * 100

    # Criação da Figura (sem plt.show para não travar a GUI)
    plt.style.use('seaborn-v0_8-darkgrid')  # Estilo mais bonito
    fig = plt.Figure(figsize=(10, 5), dpi=100)
    ax = fig.add_subplot(111)

    for t in tickers:
        # Garante que temos dados para plotar
        if t in dados_normalizados.columns:
            ax.plot(dados_normalizados.index,
                    dados_normalizados[t], label=t, linewidth=2)

    ax.set_title("Corrida de Rentabilidade (Base 100 = Início)",
                 fontsize=12, fontweight='bold')
    ax.set_xlabel("Data")
    ax.set_ylabel("Rentabilidade (%)")
    ax.axhline(100, color='black', linestyle='--', alpha=0.5, linewidth=1)
    ax.legend()

    # Ajusta datas no eixo X
    fig.autofmt_xdate()

    return relatorio_texto, fig
