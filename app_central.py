import analista_noticias
import analista_pesq
import gerenciador_carteira
import analista_agente
import analista_comp
import analista_tec
import analista_fund
import analista_valuation
import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import yfinance as yf
import os
import shutil
import certifi

# --- FORÇAR GRÁFICOS ESCUROS ---
plt.style.use('dark_background')

# --- BLOCO DE CORREÇÃO DE CERTIFICADO ---


def corrigir_certificado_ssl():
    try:
        caminho_original = certifi.where()
        caminho_seguro = os.path.join("C:\\Users\\Public", "cacert.pem")
        if not os.path.exists(caminho_seguro):
            shutil.copy(caminho_original, caminho_seguro)
        os.environ['SSL_CERT_FILE'] = caminho_seguro
        os.environ['REQUESTS_CA_BUNDLE'] = caminho_seguro
        os.environ['CURL_CA_BUNDLE'] = caminho_seguro
    except Exception as e:
        print(f"Aviso SSL: {e}")


corrigir_certificado_ssl()
# ----------------------------------------

ctk.set_appearance_mode("Dark")

# Paleta Estilizada
COR_FUNDO = "#0D0D0D"
COR_SIDEBAR = "#050505"
COR_LARANJA = "#FF6B00"
COR_LARANJA_ESCURO = "#CC5500"
COR_CARD = "#1A1A1A"


class CentralInvestidorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Central do Investidor | Pro Terminal")
        self.geometry("1200x800")
        self.configure(fg_color=COR_FUNDO)

        # --- DESIGN GEOMÉTRICO (FUNDO) ---
        # Criamos um Canvas por trás de tudo para desenhar os triângulos e quadrados
        self.bg_canvas = ctk.CTkCanvas(
            self, bg=COR_FUNDO, highlightthickness=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # NOVO: Em vez de desenhar uma vez, ele vai redesenhar sempre que a tela mudar de tamanho!
        self.bg_canvas.bind("<Configure>", self.redesenhar_geometria)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ==========================================
        # SIDEBAR (MENU LATERAL)
        # ==========================================
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0,
                                    fg_color=COR_SIDEBAR, border_width=1, border_color="#333")
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.logo = ctk.CTkLabel(
            self.sidebar, text="CENTRAL\nINVESTIDOR",
            font=ctk.CTkFont(family="Helvetica", size=22, weight="bold"), text_color=COR_LARANJA
        )
        self.logo.grid(row=0, column=0, padx=20, pady=(30, 40))

        btn_kwargs = {
            "fg_color": "transparent", "text_color": "#FFF", "hover_color": COR_LARANJA_ESCURO,
            "anchor": "w", "font": ctk.CTkFont(size=14, weight="bold"), "height": 40
        }

        self.btn_analista = ctk.CTkButton(
            self.sidebar, text="  ►  Raio-X", command=self.mostrar_tela_analista, **btn_kwargs)
        self.btn_analista.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.btn_batalha = ctk.CTkButton(
            self.sidebar, text="  ►  Batalha", command=self.mostrar_tela_batalha, **btn_kwargs)
        self.btn_batalha.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.btn_agente = ctk.CTkButton(
            self.sidebar, text="  ►  Auditor da Carteira", command=self.mostrar_tela_agente, **btn_kwargs)
        self.btn_agente.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.btn_carteira = ctk.CTkButton(
            self.sidebar, text="  ►  Carteira", command=self.mostrar_tela_carteira, **btn_kwargs)
        self.btn_carteira.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        self.btn_pesquisa = ctk.CTkButton(
            self.sidebar, text="  ►  Radar de Mercado", command=self.mostrar_tela_pesquisa, **btn_kwargs)
        self.btn_pesquisa.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

        self.lbl_disclaimer = ctk.CTkLabel(
            self.sidebar,
            text="*Software educacional.\nNão é recomendação\nde investimento.",
            font=ctk.CTkFont(size=10),
            text_color="#555555",
            justify="center"
        )
        self.lbl_disclaimer.grid(
            row=8, column=0, padx=10, pady=(50, 10), sticky="s")

        # ==========================================
        # ÁREA DE CONTEÚDO (Frames sobrepostos)
        # ==========================================
        frame_kwargs = {"corner_radius": 0, "fg_color": "transparent"}
        self.frame_analista = ctk.CTkFrame(self, **frame_kwargs)
        self.frame_batalha = ctk.CTkFrame(self, **frame_kwargs)
        self.frame_agente = ctk.CTkFrame(self, **frame_kwargs)
        self.frame_carteira = ctk.CTkFrame(self, **frame_kwargs)
        self.frame_pesquisa = ctk.CTkFrame(self, **frame_kwargs)

        self.mostrar_tela_analista()

    def redesenhar_geometria(self, event=None):
        """Redesenha as formas dinamicamente ancoradas nas bordas sempre que a tela muda de tamanho"""
        self.bg_canvas.delete("all")  # Limpa os desenhos antigos

        # Pega a largura (w) e altura (h) ATUAIS da tela
        w = event.width if event else self.bg_canvas.winfo_width()
        h = event.height if event else self.bg_canvas.winfo_height()

        if w < 100 or h < 100:
            return  # Evita erros quando a janela está minimizada

        # --- 1. CANTO SUPERIOR DIREITO ---
        self.bg_canvas.create_polygon(
            w - 300, 0, w, 0, w, 250, fill="#151515", outline="")
        self.bg_canvas.create_rectangle(
            w - 100, 40, w - 60, 80, fill=COR_LARANJA, outline="")
        self.bg_canvas.create_polygon(
            w - 120, 30, w - 100, 30, w - 110, 50, fill=COR_LARANJA_ESCURO, outline="")

        # --- 2. CANTO INFERIOR DIREITO ---
        self.bg_canvas.create_polygon(
            w - 250, h, w, h - 250, w, h, fill="#111111", outline="")
        self.bg_canvas.create_polygon(
            w - 80, h, w, h - 80, w, h, fill=COR_LARANJA_ESCURO, outline="")

        # --- 3. MEIO EM CIMA E EM BAIXO ---
        centro_x = (w + 220) / 2

        self.bg_canvas.create_polygon(
            centro_x - 120, 0, centro_x + 120, 0, centro_x, 80, fill="#121212", outline="")
        self.bg_canvas.create_polygon(
            centro_x - 150, h, centro_x + 150, h, centro_x, h - 100, fill="#121212", outline="")

        # --- 4. O SEGREDO DA TELA CHEIA (SUPERIOR ESQUERDA) ---
        if w > 1300:
            # CORRIGIDO: Usando o laranja mais escuro e removendo a linha do "furo" preto
            self.bg_canvas.create_polygon(
                220, 0, 350, 0, 220, 130, fill=COR_LARANJA_ESCURO, outline="")

    # --- LÓGICA DE TROCA DE TELAS ---

    def esconder_todos(self):
        self.frame_analista.grid_forget()
        self.frame_batalha.grid_forget()
        self.frame_agente.grid_forget()
        self.frame_carteira.grid_forget()
        self.frame_pesquisa.grid_forget()

    def mostrar_tela_analista(self):
        self.esconder_todos()
        self.frame_analista.grid(
            row=0, column=1, sticky="nsew", padx=30, pady=30)
        self._construir_analista()

    def mostrar_tela_batalha(self):
        self.esconder_todos()
        self.frame_batalha.grid(
            row=0, column=1, sticky="nsew", padx=30, pady=30)
        if not self.frame_batalha.winfo_children():
            self._construir_batalha()

    def mostrar_tela_agente(self):
        self.esconder_todos()
        self.frame_agente.grid(
            row=0, column=1, sticky="nsew", padx=30, pady=30)
        if not self.frame_agente.winfo_children():
            self._construir_agente()

    def mostrar_tela_carteira(self):
        self.esconder_todos()
        self.frame_carteira.grid(
            row=0, column=1, sticky="nsew", padx=30, pady=30)
        self._construir_carteira()

    def mostrar_tela_pesquisa(self):
        self.esconder_todos()
        self.frame_pesquisa.grid(
            row=0, column=1, sticky="nsew", padx=30, pady=30)
        if not self.frame_pesquisa.winfo_children():
            self._construir_pesquisa()

    # ==========================================
    # TELA 1: ANALISTA INDIVIDUAL
    # ==========================================
    def _construir_analista(self):
        for widget in self.frame_analista.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.frame_analista, text="RAIO-X COMPLETO DO ATIVO", font=(
            "Helvetica", 20, "bold"), text_color=COR_LARANJA).pack(anchor="w", pady=(0, 10))

        # --- BARRA DE INPUTS ---
        frame_input = ctk.CTkFrame(self.frame_analista, fg_color="transparent")
        frame_input.pack(fill="x", pady=10)

        favoritos = gerenciador_carteira.carregar_carteira()
        valores_combo = ["Selecionar Favorito..."] + favoritos

        self.combo_favoritos = ctk.CTkComboBox(
            frame_input, values=valores_combo, width=180, command=self.ao_selecionar_favorito,
            fg_color=COR_CARD, border_color=COR_LARANJA, button_color=COR_LARANJA, button_hover_color=COR_LARANJA_ESCURO)
        self.combo_favoritos.pack(side="left", padx=(0, 5))

        ctk.CTkLabel(frame_input, text="ou").pack(side="left", padx=5)

        self.entry_ticker = ctk.CTkEntry(
            frame_input, placeholder_text="Ex: VALE3", width=100,
            fg_color=COR_CARD, border_color="#333333")
        self.entry_ticker.pack(side="left", padx=5)

        # --- NOVO: CAIXA DE ESCOLHA DE PERÍODO ---
        ctk.CTkLabel(frame_input, text="Período:").pack(
            side="left", padx=(15, 5))

        self.combo_periodo = ctk.CTkComboBox(
            frame_input, values=["1mo", "3mo", "6mo", "1y", "2y", "5y"], width=80,
            fg_color=COR_CARD, border_color="#333333")
        self.combo_periodo.set("1y")  # Padrão de 1 ano
        self.combo_periodo.pack(side="left", padx=5)

        ctk.CTkButton(
            frame_input, text="Analisar Ativo", command=self.acao_analisar,
            fg_color=COR_LARANJA, hover_color=COR_LARANJA_ESCURO, font=(
                "Arial", 12, "bold")
        ).pack(side="left", padx=15)

        # --- ÁREA SCROLLABLE ---
        self.scroll_analista = ctk.CTkScrollableFrame(
            self.frame_analista, fg_color="transparent")
        self.scroll_analista.pack(fill="both", expand=True, pady=5)

        # 1. Fundamentos Básicos
        ctk.CTkLabel(self.scroll_analista, text="📋 Fundamentos", font=(
            "Arial", 14, "bold"), text_color="#FFF").pack(anchor="w", pady=(10, 0))
        self.txt_fundamentos = ctk.CTkTextbox(
            self.scroll_analista, height=80, fg_color=COR_CARD, border_color=COR_LARANJA, border_width=1)
        self.txt_fundamentos.pack(fill="x", pady=5)

        # 2. Valuation e Dividendos
        ctk.CTkLabel(self.scroll_analista, text="⚖️ Valuation & Dividendos", font=(
            "Arial", 14, "bold"), text_color="#FFF").pack(anchor="w", pady=(15, 0))
        self.txt_valuation = ctk.CTkTextbox(
            self.scroll_analista, height=180, fg_color=COR_CARD, border_color="#333", border_width=1, font=("Courier", 13))
        self.txt_valuation.pack(fill="x", pady=5)

        self.area_grafico_div = ctk.CTkFrame(
            self.scroll_analista, fg_color="transparent", height=300)
        self.area_grafico_div.pack(fill="x", pady=5)

        # 3. Gráfico Técnico e Projeção (NOVO LAYOUT)
        frame_titulo_grafico = ctk.CTkFrame(
            self.scroll_analista, fg_color="transparent")
        frame_titulo_grafico.pack(fill="x", pady=(20, 0))

        ctk.CTkLabel(frame_titulo_grafico, text="📈 Análise Técnica & Projeção", font=(
            "Arial", 14, "bold"), text_color="#FFF").pack(side="left")

        # Etiqueta que mostrará a Projeção Matemática
        self.lbl_projecao = ctk.CTkLabel(frame_titulo_grafico, text="", font=(
            "Arial", 14, "bold"), text_color=COR_LARANJA)
        self.lbl_projecao.pack(side="right", padx=10)

        self.area_grafico_individual = ctk.CTkFrame(
            self.scroll_analista, fg_color="transparent", height=400)
        self.area_grafico_individual.pack(fill="x", pady=5)

        # 4. Notícias
        ctk.CTkLabel(self.scroll_analista, text="📰 Contexto de Mercado (IA)", font=(
            "Arial", 14, "bold"), text_color="#FFF").pack(anchor="w", pady=(20, 0))
        self.frame_botoes_noticias = ctk.CTkFrame(
            self.scroll_analista, fg_color="transparent")
        self.frame_botoes_noticias.pack(fill="x", pady=5)

        ctk.CTkButton(
            self.frame_botoes_noticias, text="🌍 Panorama IBOV", command=self.acao_panorama_ibov,
            fg_color="transparent", border_width=1, border_color=COR_LARANJA, hover_color="#333", text_color=COR_LARANJA
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            self.frame_botoes_noticias, text="📰 Notícias IA do Ativo", command=self.acao_noticias,
            fg_color="transparent", border_width=1, border_color="#FFF", hover_color="#333"
        ).pack(side="left", padx=10)

        self.txt_noticias = ctk.CTkTextbox(
            self.scroll_analista, height=120, fg_color=COR_CARD, border_color="#333", border_width=1)
        self.txt_noticias.pack(fill="x", pady=(5, 20))

    def ao_selecionar_favorito(self, escolha):
        if escolha != "Selecionar Favorito...":
            self.entry_ticker.delete(0, "end")
            self.entry_ticker.insert(0, escolha)

    def acao_analisar(self):
        ticker = self.entry_ticker.get().upper()
        if not ticker.endswith(".SA"):
            ticker += ".SA"

        self.txt_fundamentos.delete("0.0", "end")
        self.txt_fundamentos.insert("0.0", "A extrair dados da B3...")
        self.txt_valuation.delete("0.0", "end")
        self.txt_valuation.insert("0.0", "A processar Valuation...")
        self.lbl_projecao.configure(text="Calculando projeção...")
        self.update()

        # 1. Fundamentos
        try:
            acao = yf.Ticker(ticker)
            dados = analista_fund.RelatorioFundamentalista(**acao.info)
            resumo = f"■ {dados.nome}\nPreço Atual: R$ {dados.preco}\n"
            resumo += f"P/L: {dados.pl_formatado}  |  ROE: {dados.roe_formatado}  |  DY: {dados.dy_formatado}"
            self.txt_fundamentos.delete("0.0", "end")
            self.txt_fundamentos.insert("0.0", resumo)
        except Exception as e:
            self.txt_fundamentos.delete("0.0", "end")
            self.txt_fundamentos.insert("0.0", f"Erro nos fundamentos: {e}")

        # 2. Valuation e Dividendos
        try:
            texto_val, fig_div = analista_valuation.gerar_analise_valuation(
                ticker)
            self.txt_valuation.delete("0.0", "end")
            self.txt_valuation.insert("0.0", texto_val)
            if fig_div:
                self.embeddar_grafico(fig_div, self.area_grafico_div)
            else:
                for widget in self.area_grafico_div.winfo_children():
                    widget.destroy()
        except Exception as e:
            self.txt_valuation.insert("end", f"\nErro no valuation: {e}")

        # 3. Gráfico Técnico e PROJEÇÃO
        try:
            # Puxa o período que escolheste ("1mo", "6mo", etc)
            periodo_selecionado = self.combo_periodo.get()

            # Agora a função retorna a Figura E o Texto da Projeção!
            fig_tec, texto_proj = analista_tec.criar_grafico(
                ticker, periodo=periodo_selecionado)

            if fig_tec:
                self.embeddar_grafico(fig_tec, self.area_grafico_individual)
                # Atualiza a etiqueta laranja com o preço alvo!
                self.lbl_projecao.configure(text=texto_proj)
            else:
                self.lbl_projecao.configure(text="Não foi possível projetar.")
        except Exception as e:
            self.lbl_projecao.configure(text=f"Erro Técnico: {e}")

    def acao_panorama_ibov(self):
        self.txt_noticias.delete("0.0", "end")
        self.txt_noticias.insert("0.0", "Carregando panorama...")
        self.update()
        panorama = analista_noticias.buscar_panorama_ibovespa()
        self.txt_noticias.delete("0.0", "end")
        self.txt_noticias.insert("0.0", panorama)

    def acao_noticias(self):
        ticker = self.entry_ticker.get().upper()
        if not ticker.endswith(".SA"):
            ticker += ".SA"
        self.txt_noticias.delete("0.0", "end")
        self.txt_noticias.insert("0.0", f"Buscando notícias...")
        self.update()
        resumo_ia = analista_noticias.buscar_contexto_atual(ticker)
        self.txt_noticias.delete("0.0", "end")
        self.txt_noticias.insert("0.0", resumo_ia)

    # ==========================================
    # TELA 2: BATALHA DE AÇÕES
    # ==========================================
    checkboxes_carteira = []

    def _construir_batalha(self):
        for widget in self.frame_batalha.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.frame_batalha, text="ARENA DE BATALHA", font=(
            "Helvetica", 24, "bold"), text_color=COR_LARANJA).pack(pady=(0, 5))

        frame_selecao = ctk.CTkFrame(
            self.frame_batalha, fg_color="transparent")
        frame_selecao.pack(fill="x")

        ctk.CTkLabel(frame_selecao, text="1. Da sua Carteira:",
                     font=("Arial", 14, "bold")).pack(anchor="w")
        scroll_carteira = ctk.CTkScrollableFrame(
            frame_selecao, height=120, fg_color=COR_CARD, border_color=COR_LARANJA, border_width=1)
        scroll_carteira.pack(fill="x", pady=5)

        self.checkboxes_carteira = []
        favoritos = gerenciador_carteira.carregar_carteira()
        if not favoritos:
            ctk.CTkLabel(scroll_carteira,
                         text="Sua carteira está vazia.").pack(pady=10)
        else:
            for ticker in favoritos:
                var = ctk.StringVar(value="")
                chk = ctk.CTkCheckBox(scroll_carteira, text=ticker, variable=var, onvalue=ticker, offvalue="",
                                      fg_color=COR_LARANJA, hover_color=COR_LARANJA_ESCURO)
                chk.pack(anchor="w", padx=10, pady=5)
                self.checkboxes_carteira.append(var)

        ctk.CTkLabel(frame_selecao, text="2. Inserir Manualmente:", font=(
            "Arial", 14, "bold")).pack(anchor="w", pady=(15, 5))
        # CORREÇÃO: Sem focus_border_color
        self.entry_batalha_externa = ctk.CTkEntry(
            frame_selecao, placeholder_text="Ex: MGLU3 KLBN11", width=400,
            fg_color=COR_CARD, border_color="#333")
        self.entry_batalha_externa.pack(fill="x", pady=5)

        ctk.CTkButton(self.frame_batalha, text="INICIAR COMBATE", fg_color=COR_LARANJA, hover_color=COR_LARANJA_ESCURO,
                      height=45, font=("Arial", 16, "bold"), command=self.acao_batalha).pack(pady=20)

        self.txt_batalha = ctk.CTkTextbox(
            self.frame_batalha, height=120, fg_color=COR_CARD, border_color="#333", border_width=1)
        self.txt_batalha.pack(fill="x", pady=5)

        self.area_grafico_batalha = ctk.CTkFrame(
            self.frame_batalha, fg_color="transparent")
        self.area_grafico_batalha.pack(fill="both", expand=True, pady=10)

    def acao_batalha(self):
        lutadores = [var.get()
                     for var in self.checkboxes_carteira if var.get()]
        externos_txt = self.entry_batalha_externa.get().upper()
        if externos_txt:
            for t in externos_txt.replace(",", " ").split():
                ticker_limpo = t.strip() + ".SA" if not t.strip().endswith(".SA") else t.strip()
                lutadores.append(ticker_limpo)

        lutadores = list(dict.fromkeys(lutadores))
        self.txt_batalha.delete("0.0", "end")

        if len(lutadores) < 2 or len(lutadores) > 10:
            self.txt_batalha.insert(
                "0.0", f"Erro: Selecione entre 2 e 10 ativos. (Atuais: {len(lutadores)})")
            return

        self.txt_batalha.insert("0.0", "Analisando dados, aguarde...")
        self.update()

        try:
            texto, fig = analista_comp.realizar_batalha(lutadores)
            self.txt_batalha.delete("0.0", "end")
            self.txt_batalha.insert("0.0", texto)
            if fig:
                self.embeddar_grafico(fig, self.area_grafico_batalha)
        except Exception as e:
            self.txt_batalha.insert("end", f"\nErro crítico: {e}")

    # ==========================================
    # TELA 3: AGENTE CAÇADOR
    # ==========================================
    def _construir_agente(self):
        for widget in self.frame_agente.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.frame_agente, text="AUDITOR DA CARTEIRA", font=(
            "Helvetica", 24, "bold"), text_color=COR_LARANJA).pack(anchor="w", pady=(0, 20))

        ctk.CTkButton(
            self.frame_agente, text="Iniciar Varredura",
            fg_color=COR_LARANJA, hover_color=COR_LARANJA_ESCURO, height=45, font=("Arial", 16, "bold"), command=self.acao_agente
        ).pack(fill="x", pady=(0, 20))

        self.txt_agente = ctk.CTkTextbox(
            self.frame_agente, fg_color=COR_CARD, border_color=COR_LARANJA, border_width=1, font=("Courier", 14))
        self.txt_agente.pack(fill="both", expand=True)

    def acao_agente(self):
        self.txt_agente.delete("0.0", "end")
        self.txt_agente.insert(
            "end", "Iniciando varredura na sua carteira...\n")
        self.update()
        df = analista_agente.buscar_melhores_oportunidades()
        if not df.empty:
            self.txt_agente.insert("end", "OPORTUNIDADES DETECTADAS:\n\n")
            self.txt_agente.insert("end", df.to_string(index=False))
        else:
            self.txt_agente.insert(
                "end", "\nNenhum ativo passou nos critérios hoje.")

    # ==========================================
    # TELA 4: MINHA CARTEIRA
    # ==========================================
    def _construir_carteira(self):
        for widget in self.frame_carteira.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.frame_carteira, text="GESTÃO DE CARTEIRA", font=(
            "Helvetica", 24, "bold"), text_color=COR_LARANJA).pack(anchor="w", pady=(0, 20))

        frame_add = ctk.CTkFrame(self.frame_carteira, fg_color="transparent")
        frame_add.pack(fill="x", pady=10)

        # CORREÇÃO: Sem focus_border_color
        self.entry_add_carteira = ctk.CTkEntry(
            frame_add, placeholder_text="Novo Ticker (ex: WEGE3)", width=250,
            fg_color=COR_CARD, border_color="#333")
        self.entry_add_carteira.pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            frame_add, text="Adicionar Ativo", command=self.acao_adicionar_carteira,
            fg_color="transparent", border_color=COR_LARANJA, border_width=2, text_color=COR_LARANJA, hover_color="#333"
        ).pack(side="left")

        scroll_frame = ctk.CTkScrollableFrame(
            self.frame_carteira, fg_color=COR_CARD, border_color="#333", border_width=1)
        scroll_frame.pack(fill="both", expand=True, pady=20)

        favoritos = gerenciador_carteira.carregar_carteira()
        if not favoritos:
            ctk.CTkLabel(
                scroll_frame, text="Nenhuma ação salva.").pack(pady=10)
        else:
            for ticker in favoritos:
                row = ctk.CTkFrame(scroll_frame, fg_color="transparent")
                row.pack(fill="x", pady=5)
                ctk.CTkLabel(row, text=f"■  {ticker}", font=(
                    "Arial", 16, "bold"), text_color="#FFF").pack(side="left", padx=10)
                ctk.CTkButton(row, text="Remover", width=60, fg_color="#333", hover_color="#555",
                              command=lambda t=ticker: self.acao_remover_carteira(t)).pack(side="right", padx=10)

    def acao_adicionar_carteira(self):
        ticker = self.entry_add_carteira.get()
        if ticker:
            sucesso, msg = gerenciador_carteira.adicionar_acao(ticker)
            if sucesso:
                self._construir_carteira()
            else:
                messagebox.showwarning("Aviso", msg)

    def acao_remover_carteira(self, ticker):
        sucesso, msg = gerenciador_carteira.remover_acao(ticker)
        if sucesso:
            self._construir_carteira()

    # ==========================================
    # TELA 5: IA ESTRATEGISTA
    # ==========================================
    def _construir_pesquisa(self):
        for widget in self.frame_pesquisa.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.frame_pesquisa, text="RADAR DE MERCADO", font=(
            "Helvetica", 24, "bold"), text_color=COR_LARANJA).pack(anchor="w", pady=(0, 20))

        ctk.CTkButton(
            self.frame_pesquisa, text="Gerar Relatório Macro",
            fg_color=COR_LARANJA, hover_color=COR_LARANJA_ESCURO, height=45, font=("Arial", 16, "bold"), command=self.acao_pesquisar_ia
        ).pack(fill="x", pady=(0, 20))

        self.scroll_pesquisa = ctk.CTkScrollableFrame(
            self.frame_pesquisa, fg_color="transparent")
        self.scroll_pesquisa.pack(fill="both", expand=True)

    def acao_pesquisar_ia(self):
        for widget in self.scroll_pesquisa.winfo_children():
            widget.destroy()
        lbl_carregando = ctk.CTkLabel(
            self.scroll_pesquisa, text="Sintetizando dados do mercado...", text_color=COR_LARANJA)
        lbl_carregando.pack(pady=50)
        self.update()

        relatorio = analista_pesq.pesquisar_oportunidades()
        lbl_carregando.destroy()

        if relatorio:
            frame_macro = ctk.CTkFrame(
                self.scroll_pesquisa, fg_color=COR_CARD, border_color="#333", border_width=1)
            frame_macro.pack(fill="x", pady=10)
            ctk.CTkLabel(frame_macro, text=f"CENÁRIO MACROECONÔMICO ({relatorio.data_analise})", font=(
                "Arial", 14, "bold"), text_color=COR_LARANJA).pack(anchor="w", padx=15, pady=(15, 5))
            ctk.CTkLabel(frame_macro, text=relatorio.cenario_macro, font=(
                "Arial", 14), justify="left", wraplength=800).pack(anchor="w", padx=15, pady=(0, 15))

            for acao in relatorio.sugestoes:
                self._criar_card_acao(acao)
        else:
            ctk.CTkLabel(self.scroll_pesquisa, text="Falha na IA.",
                         text_color="red").pack()

    def _criar_card_acao(self, acao):
        card = ctk.CTkFrame(
            self.scroll_pesquisa, fg_color="#1A1A1A", border_color="#333", border_width=1)
        card.pack(fill="x", pady=10)

        topo = ctk.CTkFrame(card, fg_color="transparent")
        topo.pack(fill="x", padx=15, pady=(15, 5))

        # Ticker e Nome
        ctk.CTkLabel(topo, text=acao.ticker, font=(
            "Helvetica", 18, "bold"), text_color="#FF6B00").pack(side="left")
        ctk.CTkLabel(topo, text=f" • {acao.nome_empresa} ({acao.setor})", font=(
            "Arial", 14), text_color="#AAA").pack(side="left")

        # Risco
        cor_risco = "#00FF00" if "Baixo" in acao.risco else "#FFA500" if "Médio" in acao.risco else "#FF4444"
        ctk.CTkLabel(topo, text=f"RISCO: {acao.risco.upper()}", text_color=cor_risco, font=(
            "Arial", 12, "bold")).pack(side="right")

        # --- NOVO: A Etiqueta de Foco/Perfil---
        ctk.CTkLabel(card, text=f"🏷️ Perfil: {acao.foco_investimento}", text_color="#3498DB", font=(
            "Arial", 13, "bold")).pack(anchor="w", padx=15, pady=(0, 5))

        # Tese de Investimento
        ctk.CTkLabel(card, text=acao.tese_investimento, font=(
            "Arial", 14), justify="left", wraplength=800).pack(anchor="w", padx=15, pady=5)

        # Alvo Estimado
        if acao.preco_alvo_estimado and acao.preco_alvo_estimado != "N/A":
            ctk.CTkLabel(card, text=f"🎯 Alvo Estimado: {acao.preco_alvo_estimado}", text_color="#888").pack(
                anchor="w", padx=15, pady=(0, 15))
        else:
            # Só dá um espaço no fundo se não houver alvo
            ctk.CTkFrame(card, height=10, fg_color="transparent").pack()

    def embeddar_grafico(self, fig, frame_destino):
        for widget in frame_destino.winfo_children():
            widget.destroy()
        if fig:
            fig.patch.set_facecolor(COR_FUNDO)
            canvas = FigureCanvasTkAgg(fig, master=frame_destino)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)


if __name__ == "__main__":
    app = CentralInvestidorApp()
    app.mainloop()
