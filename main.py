import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import requests
import threading
import os

# --- CONFIGURAÇÕES DO SISTEMA ---
VERSAO_ATUAL = "1.0.0" 
USUARIO_GITHUB = "Gilasexe" 
REPO_GITHUB = "TPPK-The_Personal_Pocket_Knife"   
URL_API_GITHUB = f"https://api.github.com/repos/{USUARIO_GITHUB}/{REPO_GITHUB}/releases/latest"

# Configuração visual
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue") 

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da Janela
        self.title(f"TPPK-The_Personal_Pocket_Knife - Gilasexe (v{VERSAO_ATUAL})")
        self.geometry("1000x600")

        try:
            # Descobre o caminho exato da logo
            diretorio_atual = os.path.dirname(os.path.abspath(__file__))
            caminho_logo = os.path.join(diretorio_atual, "logo.png")
            
            # Carrega e aplica a imagem como ícone da janela
            imagem_icone = tk.PhotoImage(file=caminho_logo)
            self.iconphoto(False, imagem_icone)
        except Exception as e:
            print(f"Aviso: Logo não carregada. Erro: {e}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Variáveis de Atualização
        self.atualizacao_disponivel = False
        self.versao_nuvem = VERSAO_ATUAL

        # --- DADOS DO LIVRO (Páginas e Categorias) ---
        self.conteudo_livro = {}
        self.carregar_livros_da_pasta()
        
        # Pega a primeira categoria que encontrar
        if self.conteudo_livro:
            self.categoria_atual = list(self.conteudo_livro.keys())[0]
        else:
            self.categoria_atual = "Vazio"
            self.conteudo_livro["Vazio"] = [("Livro Vazio", "Crie pastas e arquivos .txt dentro da pasta 'cadernos'.")]
            
        self.indice_pagina = 0

        # --- SISTEMA DE ATUALIZAÇÃO ---
        threading.Thread(target=self.verificar_atualizacoes_startup, daemon=True).start()

        # --- SIDEBAR (Menu Lateral) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="📓 FUNÇÕES", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(pady=30)

        self.btn_intro = ctk.CTkButton(self.sidebar_frame, text="Introdução", command=self.show_intro)
        self.btn_intro.pack(pady=10, padx=20)

        self.btn_tools = ctk.CTkButton(self.sidebar_frame, text="Ferramentas Linux", command=self.show_tools)
        self.btn_tools.pack(pady=10, padx=20)

        self.btn_livro = ctk.CTkButton(self.sidebar_frame, text="Abrir Livro", command=self.show_book)
        self.btn_livro.pack(pady=10, padx=20)

        self.btn_sair = ctk.CTkButton(self.sidebar_frame, text="Sair", fg_color="#8B0000", hover_color="#5e0000", command=self.sair_app)
        self.btn_sair.pack(side="bottom", pady=20, padx=20)

        self.btn_sistema = ctk.CTkButton(self.sidebar_frame, text="⚙️ Sistema", fg_color="#3d3d3d", command=self.abrir_painel_sistema)
        self.btn_sistema.pack(side="bottom", pady=10, padx=20)

        # --- ÁREA DE CONTEÚDO ---
        self.main_view = ctk.CTkFrame(self, corner_radius=15)
        self.main_view.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        # AGORA SIM, chama a introdução por último!
        self.show_intro()

    # ==========================================
    # LÓGICA DE PASTAS DO LIVRO
    # ==========================================
    def carregar_livros_da_pasta(self):
        diretorio_projeto = os.path.dirname(os.path.abspath(__file__))
        pasta_base = os.path.join(diretorio_projeto, "cadernos")

        if not os.path.exists(pasta_base):
            pasta_exemplo = os.path.join(pasta_base, "Exemplo_Materia")
            os.makedirs(pasta_exemplo)
            caminho_exemplo = os.path.join(pasta_exemplo, "01_Bem_Vindo.txt")
            with open(caminho_exemplo, "w", encoding="utf-8") as f:
                f.write("Título: Como usar os Cadernos\n\nPara adicionar páginas, basta criar arquivos .txt nesta pasta.\nA primeira linha do arquivo sempre será o título da página!")

        for nome_pasta in os.listdir(pasta_base):
            caminho_pasta = os.path.join(pasta_base, nome_pasta)
            if os.path.isdir(caminho_pasta):
                paginas = []
                arquivos_txt = sorted(os.listdir(caminho_pasta))
                for arquivo in arquivos_txt:
                    if arquivo.endswith(".txt"):
                        caminho_arquivo = os.path.join(caminho_pasta, arquivo)
                        with open(caminho_arquivo, "r", encoding="utf-8") as f:
                            linhas = f.readlines()
                            if linhas:
                                titulo = linhas[0].strip() 
                                conteudo = "".join(linhas[1:]).strip() 
                                paginas.append((titulo, conteudo))
                if paginas:
                    self.conteudo_livro[nome_pasta] = paginas

    # ==========================================
    # LÓGICA DE NAVEGAÇÃO
    # ==========================================
    def limpar_tela(self):
        for widget in self.main_view.winfo_children():
            widget.destroy()

    def sair_app(self):
        self.destroy()
        sys.exit()

    def show_intro(self):
        self.limpar_tela()
        titulo = ctk.CTkLabel(self.main_view, text="Bem vindo ao TPPK - Gilasexe! 🚀", font=ctk.CTkFont(size=28, weight="bold"))
        titulo.pack(pady=(40, 20))

        card_frame = ctk.CTkFrame(self.main_view, fg_color="#2b2b2b", corner_radius=10)
        card_frame.pack(pady=20, padx=40, fill="x")

        texto_intro = (
            "Este é o seu canivete suíço pessoal. Aqui está o que você pode fazer:\n\n"
            "🐧 Ferramentas Linux: Limpe seu sistema, controle a placa NVIDIA (EnvyControl)\n"
            "      e resolva problemas do Arch sem precisar decorar comandos.\n\n"
            "📚 Abrir Livro: Seus cadernos de estudo de Programação, Cálculo e Anotações.\n\n"
            "⚙️ Sistema: Baixe novas versões e scripts direto da nuvem."
        )
        ctk.CTkLabel(card_frame, text=texto_intro, font=("Arial", 16), justify="left").pack(pady=20, padx=20)

    # ==========================================
    # FERRAMENTAS LINUX
    # ==========================================
    def show_tools(self):
        self.limpar_tela()
        titulo = ctk.CTkLabel(self.main_view, text="🛠️ Ferramentas Arch Linux", font=ctk.CTkFont(size=24, weight="bold"))
        titulo.pack(pady=(20, 10))

        # CARD 1: ENVYCONTROL
        gpu_frame = ctk.CTkFrame(self.main_view, fg_color="#2b2b2b", corner_radius=10)
        gpu_frame.pack(pady=10, padx=40, fill="x")
        ctk.CTkLabel(gpu_frame, text="🎮 Controle de GPU (EnvyControl)", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(15, 5))

        try:
            status_atual = subprocess.check_output(["envycontrol", "--query"]).decode("utf-8").strip()
            texto_status = f"Modo Atual: {status_atual.upper()}"
        except:
            texto_status = "Modo Atual: Desconhecido (Instale o envycontrol)"

        ctk.CTkLabel(gpu_frame, text=texto_status, text_color="#a9a9a9", font=("Arial", 14)).pack(pady=(0, 15))

        botoes_frame = ctk.CTkFrame(gpu_frame, fg_color="transparent")
        botoes_frame.pack(pady=(0, 20))

        ctk.CTkButton(botoes_frame, text="NVIDIA (Jogo)", fg_color="#76b900", hover_color="#5a8d00", command=lambda: self.mudar_gpu("nvidia")).grid(row=0, column=0, padx=10)
        ctk.CTkButton(botoes_frame, text="HÍBRIDO (Equilíbrio)", fg_color="#b8860b", hover_color="#8b6508", command=lambda: self.mudar_gpu("hybrid")).grid(row=0, column=1, padx=10)
        ctk.CTkButton(botoes_frame, text="INTEGRADA (Bateria)", fg_color="#0071c5", hover_color="#005a9e", command=lambda: self.mudar_gpu("integrated")).grid(row=0, column=2, padx=10)

        # CARD 2: LIMPEZA
        limpeza_frame = ctk.CTkFrame(self.main_view, fg_color="#2b2b2b", corner_radius=10)
        limpeza_frame.pack(pady=20, padx=40, fill="x")
        ctk.CTkLabel(limpeza_frame, text="🧹 Faxina do Sistema", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(15, 10))
        ctk.CTkButton(limpeza_frame, text="Limpar Cache do Pacman Antigo", command=lambda: subprocess.run(["pkexec", "paccache", "-r"])).pack(pady=(0, 20))

    def mudar_gpu(self, modo):
        comando = f"pkexec envycontrol -s {modo}"
        try:
            subprocess.run(comando.split(), check=True)
            messagebox.showinfo("Sucesso!", f"Modo {modo.upper()} ativado!\n\nPor favor, reinicie o notebook.")
            self.show_tools()
        except subprocess.CalledProcessError:
            messagebox.showwarning("Cancelado", "Você cancelou a senha ou ocorreu um erro.")
        except FileNotFoundError:
            messagebox.showerror("Erro Crítico", "EnvyControl não encontrado no sistema!")

    # ==========================================
    # LEITOR DO LIVRO (Dinâmico)
    # ==========================================
    def show_book(self):
        self.limpar_tela()
        titulo = ctk.CTkLabel(self.main_view, text="📚 Leitor do Almanaque", font=ctk.CTkFont(size=24, weight="bold"))
        titulo.pack(pady=(20, 10))

        # BARRA DE NAVEGAÇÃO SUPERIOR
        nav_frame = ctk.CTkFrame(self.main_view, fg_color="transparent")
        nav_frame.pack(fill="x", padx=40, pady=5)

        ctk.CTkLabel(nav_frame, text="Matéria:", font=("Arial", 14, "bold")).pack(side="left", padx=(0, 10))
        
        self.menu_categoria = ctk.CTkOptionMenu(nav_frame, values=list(self.conteudo_livro.keys()), command=self.mudar_categoria)
        self.menu_categoria.set(self.categoria_atual)
        self.menu_categoria.pack(side="left")

        # ÁREA DE LEITURA
        leitor_frame = ctk.CTkFrame(self.main_view, fg_color="#1e1e1e", corner_radius=10)
        leitor_frame.pack(fill="both", expand=True, padx=40, pady=10)

        self.lbl_titulo_pagina = ctk.CTkLabel(leitor_frame, text="Título", font=ctk.CTkFont(size=18, weight="bold"), text_color="#5ce1e6")
        self.lbl_titulo_pagina.pack(pady=(15, 5))

        self.texto_pagina = ctk.CTkTextbox(leitor_frame, font=("Arial", 16), wrap="word", fg_color="transparent")
        self.texto_pagina.pack(fill="both", expand=True, padx=20, pady=10)

        # CONTROLES INFERIORES
        controle_frame = ctk.CTkFrame(self.main_view, fg_color="transparent")
        controle_frame.pack(fill="x", padx=40, pady=(0, 20))

        self.btn_anterior = ctk.CTkButton(controle_frame, text="< Anterior", width=100, command=self.pagina_anterior)
        self.btn_anterior.pack(side="left")

        self.lbl_contador = ctk.CTkLabel(controle_frame, text="Página X de Y", font=("Arial", 14))
        self.lbl_contador.pack(side="left", expand=True)

        self.btn_proxima = ctk.CTkButton(controle_frame, text="Próxima >", width=100, command=self.pagina_proxima)
        self.btn_proxima.pack(side="right")

        self.carregar_pagina()

    def mudar_categoria(self, nova_categoria):
        self.categoria_atual = nova_categoria
        self.indice_pagina = 0
        self.carregar_pagina()

    def pagina_proxima(self):
        total = len(self.conteudo_livro[self.categoria_atual])
        if self.indice_pagina < total - 1:
            self.indice_pagina += 1
            self.carregar_pagina()

    def pagina_anterior(self):
        if self.indice_pagina > 0:
            self.indice_pagina -= 1
            self.carregar_pagina()

    def carregar_pagina(self):
        paginas_da_categoria = self.conteudo_livro[self.categoria_atual]
        total = len(paginas_da_categoria)
        
        titulo_atual, texto_atual = paginas_da_categoria[self.indice_pagina]

        self.lbl_titulo_pagina.configure(text=titulo_atual)
        self.lbl_contador.configure(text=f"Página {self.indice_pagina + 1} de {total}")

        self.texto_pagina.configure(state="normal")
        self.texto_pagina.delete("0.0", "end")
        self.texto_pagina.insert("0.0", texto_atual)
        self.texto_pagina.configure(state="disabled")

        self.btn_anterior.configure(state="normal" if self.indice_pagina > 0 else "disabled")
        self.btn_proxima.configure(state="normal" if self.indice_pagina < total - 1 else "disabled")

    # ==========================================
    # SISTEMA E ATUALIZAÇÕES
    # ==========================================
    def verificar_atualizacoes_startup(self):
        try:
            resposta = requests.get(URL_API_GITHUB, timeout=5)
            if resposta.status_code == 200:
                dados_release = resposta.json()
                self.versao_nuvem = dados_release['tag_name'].replace('v', '')
                self.notas_atualizacao = dados_release.get('body', 'Sem notas de atualização.')
                
                if self.versao_nuvem != VERSAO_ATUAL:
                    self.atualizacao_disponivel = True
                    self.after(0, lambda: self.btn_sistema.configure(fg_color="#006400", text="⚙️ Atualização Pronta!"))
        except Exception as e:
            print(f"Erro ao checar API do GitHub: {e}")

    def abrir_painel_sistema(self):
        self.limpar_tela()
        ctk.CTkLabel(self.main_view, text="⚙️ Configurações do Sistema", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        
        info_frame = ctk.CTkFrame(self.main_view)
        info_frame.pack(pady=10, padx=40, fill="x")

        ctk.CTkLabel(info_frame, text=f"Versão Instalada: v{VERSAO_ATUAL}", font=("Arial", 16)).pack(pady=10)

        if self.atualizacao_disponivel:
            ctk.CTkLabel(info_frame, text=f"🔥 Nova versão encontrada: v{self.versao_nuvem}", text_color="#00ff00", font=("Arial", 16)).pack(pady=10)
            
            caixa_texto = ctk.CTkTextbox(info_frame, height=80)
            caixa_texto.pack(pady=10, padx=20, fill="x")
            caixa_texto.insert("0.0", f"O que há de novo:\n{self.notas_atualizacao}")
            caixa_texto.configure(state="disabled") 
            
            ctk.CTkButton(self.main_view, text="Baixar e Instalar Update", fg_color="green", hover_color="#004d00").pack(pady=20)
        else:
            ctk.CTkLabel(info_frame, text="✅ Seu Almanaque está na versão mais recente.", text_color="gray", font=("Arial", 16)).pack(pady=10)
            ctk.CTkButton(self.main_view, text="Verificar Novamente", command=self.verificar_atualizacoes_startup).pack(pady=20)

if __name__ == "__main__":
    app = App()
    app.mainloop()