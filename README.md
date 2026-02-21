# Central do Investidor 
Um terminal desktop de inteligência de mercado com design profissional para analisar ações da Bolsa Brasileira (B3). O projeto combina matemática financeira clássica (Value Investing), análise técnica preditiva e Inteligência Artificial (Google Gemini) para auxiliar na tomada de decisões de investimento.

> **⚠️ Aviso Importante:** Este projeto é uma ferramenta de assistência e análise de dados, desenvolvida para fins educacionais e de estudo. Nenhuma informação gerada por este aplicativo constitui uma recomendação de compra ou venda de ativos financeiros. Invista com responsabilidade.

## Funcionalidades

* **Raio-X Individual:** Análise completa de um ativo contendo:
  * *Valuation:* Cálculo do Preço Justo de Graham e margem de segurança.
  * *Dividendos:* Histórico de 5 anos em gráfico de barras e projeção de DY.
  * *Análise Técnica:* Gráficos dinâmicos de preços, médias móveis, RSI (IFR) e projeção futura usando Regressão Linear (apenas um chute matématico).
  * *IA:* Resumo inteligente das notícias mais recentes e seus impactos.
* **Batalha de Ações:** Compare o rendimento histórico e os fundamentos de 2 a 10 ativos lado a lado, com a IA atuando como "Juiz" para definir a melhor escolha do dia.
* **Auditor da Carteira:** Um robô matemático que varre as suas ações salvas e filtra apenas aquelas que apresentam P/L descontado, ROE alto e endividamento (Dívida/EBITDA) seguro.
* **Radar de Mercado:** A IA atua como um estrategista macroeconômico, analisando juros, inflação e geopolítica global para sugerir ativos fora do seu radar, definindo o "Perfil" (ex: Foco em Dividendos ou Crescimento).
* **Gestão de Carteira:** Salve seus ativos favoritos em um banco de dados local simples (`JSON`) para acesso rápido em todas as outras ferramentas.

---

## Pré-requisitos de Hardware e Software

1.  **Sistema Operacional:** Windows, macOS ou Linux.
2.  **Python:** Versão **3.8 ou superior**.
3.  **Conexão com a Internet:** Obrigatório para baixar cotações em tempo real (Yahoo Finance) e comunicar com a IA (Google Gemini).

---

## Instalação

### 1. Clone ou baixe o projeto
Crie uma pasta, coloque os arquivos do projeto lá e abra o terminal nessa pasta.

### 2. Crie o Ambiente Virtual
Recomenda-se o uso de um ambiente virtual para evitar conflitos de bibliotecas.
```bash
python -m venv venv
.\venv\Scripts\activate   # No Windows
# source venv/bin/activate # No Linux/Mac

```
---

## Instale as Bibliotecas Necessárias
Instale todas as dependências em um único comando dentro do venv:
```bash
pip install customtkinter yfinance pandas matplotlib numpy google-generativeai python-dotenv pydantic certifi
#ou 
#pip install -r requirements.txt

```
---

## Configuração

### 1. Chave da API do Google Gemini
Para que o Juiz, o Radar de Mercado e o resumo de notícias funcionem, você precisa de uma chave gratuita do Google AI Studio.
Crie um arquivo chamado .env na mesma pasta do projeto e adicione a sua chave:
GOOGLE_API_KEY=sua_chave_aqui_colada_do_google_aistudio

### 2. Certificados SSL (Fix para Windows)
O projeto já inclui um bloco de código autossuficiente no arquivo principal para corrigir erros de certificado SSL (Erro curl 77) comuns no Windows. O sistema criará automaticamente uma cópia segura dos certificados em C:\Users\Public\cacert.pem. Nenhuma ação manual é necessária.

---

## Como usar

### 1.Ative o ambiente virtual (se ainda não estiver ativo):
```bash
.\venv\Scripts\activate

```

### 2.Inicie a Central do Investidor:
```bash 
python app_central.py

```

### 3.Navegação:
Utilize o menu lateral esquerdo para navegar entre a Análise Individual, a Batalha de Ações, o Auditor da sua Carteira e o Radar de Mercado. Comece adicionando alguns ativos na aba "Carteira"!
