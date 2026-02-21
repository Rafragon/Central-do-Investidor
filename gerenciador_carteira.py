import json
import os

ARQUIVO_CARTEIRA = "minha_carteira.json"


def carregar_carteira():
    """Lê o arquivo JSON e retorna uma lista de tickers."""
    if not os.path.exists(ARQUIVO_CARTEIRA):
        return []
    try:
        with open(ARQUIVO_CARTEIRA, "r") as f:
            dados = json.load(f)
            return dados.get("tickers", [])
    except Exception as e:
        print(f"Erro ao carregar carteira: {e}")
        return []


def adicionar_acao(ticker):
    """Adiciona um ticker à lista e salva."""
    lista = carregar_carteira()
    ticker = ticker.upper().strip()

    # Garante o sufixo .SA
    if not ticker.endswith(".SA"):
        ticker += ".SA"

    if ticker not in lista:
        lista.append(ticker)
        _salvar(lista)
        return True, f"{ticker} adicionado!"
    else:
        return False, f"{ticker} já está na carteira."


def remover_acao(ticker):
    """Remove um ticker da lista e salva."""
    lista = carregar_carteira()
    if ticker in lista:
        lista.remove(ticker)
        _salvar(lista)
        return True, f"{ticker} removido!"
    return False, "Ticker não encontrado."


def _salvar(lista):
    """Função interna para escrever no arquivo JSON."""
    with open(ARQUIVO_CARTEIRA, "w") as f:
        json.dump({"tickers": lista}, f, indent=4)
