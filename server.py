import sys
import tkinter as tk

# ==============================================================================
# CORREÇÃO CRÍTICA DE COMPATIBILIDADE PARA PYTHON 3.13 / 3.14
# ==============================================================================
import types
if 'tkinter.tix' not in sys.modules:
    tix_falso = types.ModuleType("tkinter.tix")
    tix_falso.Tk = tk.Tk
    tix_falso.Grid = tk.Grid
    tix_falso.Pack = tk.Pack
    tix_falso.Place = tk.Place
    sys.modules["tkinter.tix"] = tix_falso
# ==============================================================================

import math
import os
import random
import re
import subprocess
import threading
import time
import json
import base64
import unicodedata
from PIL import Image, ImageTk
import requests
from tkinter import messagebox, simpledialog, Toplevel
import customtkinter as ctk

# SUPORTE PARA ARRASTAR E LARGAR FICHEIROS
from tkinterdnd2 import DND_FILES, TkinterDnD

# Configuração global de aparência
ctk.set_appearance_mode("Dark")

class FFKaraokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FF KARAOKE - Painel de Controlo")
        self.root.geometry("620x950")
        self.root.configure(bg="#0b0b0d") 

        # Variáveis de Controle
        self.playlist = []
        self.auto_play = False
        self.aguardando_contagem = False
        self.musica_preparada = None
        self.link_catalogo = "https://ffkaraoke.streamlit.app/"
        self.pasta_sistema = r"G:\F.F KARAOKE"
        
        # Caminho para o ficheiro de salvamento automático
        self.arquivo_backup = os.path.join(self.pasta_sistema, "playlist_backup.json")

        self.miniatura_tk = None
        try:
            caminho_foto = os.path.join(self.pasta_sistema, "foto_cantor.png")
            if os.path.exists(caminho_foto):
                img_padrao = Image.open(caminho_foto).resize((60, 60), Image.Resampling.LANCZOS)
                self.miniatura_tk = ImageTk.PhotoImage(img_padrao)
        except Exception as e:
            print(f"Nota: Erro ao carregar miniatura: {e}")

        # Efeitos Visuais
        self.imagem_fundo_tk = None
        self.pedidos_nuvem_cache = []
        self.piscar_ativo = False
        self.cor_atual_pisca = "#fff200"
        
        self.intensidade_fade = 1.0 
        self.direcao_fade = -0.05 

        self.url_firebase = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"

        self.inicializar_voz_maria_natural()
        
        # Criação correta da Janela do Público
        self.janela_publico = tk.Toplevel(self.root)
        self.janela_publico.title("FF KARAOKE - Ecrã Principal")
        self.janela_publico.geometry("1024x768")
        self.janela_publico.configure(bg="#0b0b0d")

        self.canvas_logo = tk.Canvas(self.janela_publico, bg="#0b0b0d", highlightthickness=0)
        self.canvas_logo.pack(expand=True, fill="both")

        self.carregar_template_fundo()
        self.janela_publico.bind("<Double-Button-1>", self.alternar_tela_cheia)
        self.tela_cheia = False

        self.criar_interface_operador()
        
        # Carregar playlist guardada anteriormente (se existir)
        self.carregar_playlist_memoria()

        self.verificar_novos_pedidos_cloud()
        self.executar_ciclo_fade()
        
        self.root.protocol("WM_DELETE_WINDOW", self.fechar_aplicativo)

    def salvar_playlist_memoria(self):
        try:
            if not os.path.exists(self.pasta_sistema):
                os.makedirs(self.pasta_sistema, exist_ok=True)
            with open(self.arquivo_backup, "w", encoding="utf-8") as f:
                json.dump(self.playlist, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Erro ao salvar backup da playlist: {e}")

    def carregar_playlist_memoria(self):
        try:
            if os.path.exists(self.arquivo_backup):
                with open(self.arquivo_backup, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    if isinstance(dados, list):
                        self.playlist = dados
                        self.atualizar_listas_interface()
        except Exception as e:
            print(f"Erro ao carregar backup da playlist: {e}")

    def alternar_auto_play(self):
        self.auto_play = not self.auto_play
        estado = "LIGADO" if self.auto_play else "DESLIGADO"
        self.btn_auto.configure(text=f"🔄 AUTO-PLAY: {estado}", fg_color="#1b3d22" if self.auto_play else "#555555")

    def executar_ciclo_fade(self):
        self.intensidade_fade += self.direcao_fade
        if self.intensidade_fade <= 0.3 or self.intensidade_fade >= 1.0:
            self.direcao_fade *= -1
        self.root.after(50, self.executar_ciclo_fade)

    def alternar_tela_cheia(self, event=None):
        self.tela_cheia = not self.tela_cheia
        self.janela_publico.attributes("-fullscreen", self.tela_cheia)

    def carregar_template_fundo(self):
        caminho_fundo = os.path.join(self.pasta_sistema, "fundo_publico.png")
        try:
            if os.path.exists(caminho_fundo):
                img = Image.open(caminho_fundo).resize((1024, 768), Image.Resampling.LANCZOS)
                self.imagem_fundo_tk = ImageTk.PhotoImage(img)
                self.canvas_logo.delete("imagem_fundo")
                self.canvas_logo.create_image(0, 0, image=self.imagem_fundo_tk, anchor="nw", tags="imagem_fundo")
                self.canvas_logo.tag_lower("imagem_fundo")
        except Exception as e: 
            print(f"Erro ao carregar fundo: {e}")

    def inicializar_voz_maria_natural(self):
        try:
            import pyttsx3
            self.engine_voz = pyttsx3.init()
            self.engine_voz.setProperty("rate", 165)
            voices = self.engine_voz.getProperty("voices")
            for voice in voices:
                if "portuguese" in voice.name.lower():
                    self.engine_voz.setProperty("voice", voice.id)
                    return
        except: 
            self.engine_voz = None

    def falar_em_fio(self, texto, callback_funcao=None):
        if hasattr(self, 'engine_voz') and self.engine_voz:
            def t():
                try:
                    self.engine_voz.say(texto)
                    self.engine_voz.runAndWait()
                except: 
                    pass
                if callback_funcao: 
                    self.root.after(10, callback_funcao)
            threading.Thread(target=t, daemon=True).start()
        elif callback_funcao: 
            self.root.after(10, callback_funcao)

    def criar_interface_operador(self):
        self.aba_fila = ctk.CTkFrame(self.root, fg_color="transparent")
        self.aba_fila.pack(fill="both", expand=True, padx=15, pady=10)
        
        ctk.CTkLabel(self.aba_fila, text="SISTEMA DE GESTÃO DE PEDIDOS LOCAL", font=("Arial", 14, "bold"), text_color="#d4af37").pack(pady=2)
        
        self.btn_auto = ctk.CTkButton(self.aba_fila, text="🔄 AUTO-PLAY: DESLIGADO", fg_color="#555555", font=("Arial", 11, "bold"), command=self.alternar_auto_play)
        self.btn_auto.pack(pady=4)
        
        frame_form = ctk.CTkFrame(self.aba_fila, fg_color="#141416", border_color="#d4af37", border_width=1)
        frame_form.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(frame_form, text="Nome do Cantor:", text_color="#ffffff", font=("Arial", 11)).pack(anchor="w", padx=15, pady=1)
        self.entry_cantor = ctk.CTkEntry(frame_form, placeholder_text="Ex: Pedro", height=28)
        self.entry_cantor.pack(fill="x", padx=15, pady=3)
        
        ctk.CTkLabel(frame_form, text="Nome da Música:", text_color="#ffffff", font=("Arial", 11)).pack(anchor="w", padx=15, pady=1)
        self.entry_musica = ctk.CTkEntry(frame_form, placeholder_text="Ex: Euclides da Lomba", height=28)
        self.entry_musica.pack(fill="x", padx=15, pady=3)
        
        ctk.CTkButton(frame_form, text="★ ADICIONAR À LISTA LOCAL", fg_color="#1b3d22", text_color="white", font=("Arial", 11, "bold"), height=30, command=self.adicionar_musica_manual).pack(fill="x", padx=15, pady=8)
        
        ctk.CTkLabel(self.aba_fila, text="FILA DE REPRODUÇÃO ATUAL:", font=("Arial", 11, "bold"), text_color="#ffffff").pack(anchor="w", padx=5, pady=2)
        
        self.lista_visual = tk.Listbox(self.aba_fila, bg="#141416", fg="white", selectbackground="#d4af37", font=("Arial", 11), bd=0, highlightthickness=1, highlightbackground="#333333", height=6)
        self.lista_visual.pack(fill="x", padx=5, pady=2)
        
        try:
            self.lista_visual.drop_target_register(DND_FILES)
            self.lista_visual.dnd_bind("<<Drop>>", self.processar_arquivo_arrastado)
        except Exception as e:
            print(f"Aviso: Drag and Drop não suportado nesta plataforma: {e}")

        frame_ctrl = ctk.CTkFrame(self.aba_fila, fg_color="transparent")
        frame_ctrl.pack(fill="x", padx=5, pady=2)
        
        ctk.CTkButton(frame_ctrl, text="↑ Subir", width=90, fg_color="#2b1b3d", command=self.mover_para_cima).pack(side=tk.LEFT, padx=2)
        ctk.CTkButton(frame_ctrl, text="↓ Descer", width=90, fg_color="#2b1b3d", command=self.mover_para_baixo).pack(side=tk.LEFT, padx=2)
        ctk.CTkButton(frame_ctrl, text="🗑 Remover", width=90, fg_color="#5a1818", command=self.remover_musica_selecionada).pack(side=tk.RIGHT, padx=2)
        
        self.btn_lancar = ctk.CTkButton(self.aba_fila, text="► ANUNCIAR PRÓXIMO CANTOR", fg_color="#d4af37", text_color="black", font=("Arial", 13, "bold"), height=42, command=self.gerenciar_clique_transicao)
        self.btn_lancar.pack(fill="x", padx=5, pady=8)
        
        # Área Nuvem
        frame_nuvem_box = ctk.CTkFrame(self.aba_fila, fg_color="#1a1a1e", border_color="#e74c3c", border_width=1)
        frame_nuvem_box.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.lbl_alerta = ctk.CTkLabel(frame_nuvem_box, text="SISTEMA EM SINTONIA CLOUD (Clique duplo para enviar à fila)", fg_color="#333333", text_color="white", font=("Arial", 11, "bold"), height=25)
        self.lbl_alerta.pack(fill="x", padx=5, pady=2)
        
        self.lista_mensagens = tk.Listbox(frame_nuvem_box, bg="#141416", fg="#00ffcc", selectbackground="#d4af37", font=("Arial", 10, "bold"), bd=0)
        self.lista_mensagens.pack(fill="both", expand=True, padx=5, pady=2)
        
        ctk.CTkButton(frame_nuvem_box, text="🗑 Remover Pedido Nuvem", fg_color="#5a1818", height=25, command=self.remover_pedido_nuvem).pack(fill="x", padx=5, pady=5)
        
        self.lista_mensagens.bind("<Double-Button-1>", self.acao_adicionar_pedido_nuvem)

    def verificar_novos_pedidos_cloud(self):
        def tarefa_busca():
            try:
                resposta = requests.get(self.url_firebase, timeout=5)
                if resposta.status_code == 200 and resposta.json():
                    self.root.after(10, lambda: self.processar_resposta_firebase(resposta.json()))
            except: 
                pass
            self.root.after(4000, self.verificar_novos_pedidos_cloud)
        threading.Thread(target=tarefa_busca, daemon=True).start()

    def processar_resposta_firebase(self, dados_json):
        if not dados_json:
            return
        for id_fb, dados in dados_json.items():
            if not any(p["id"] == id_fb for p in self.pedidos_nuvem_cache):
                cantor = dados.get("cantor", "Anónimo").strip()
                musica = dados.get("musica", "Música Indefinida").strip()
                self.pedidos_nuvem_cache.append({"id": id_fb, "cantor": cantor, "musica": musica})
                self.lista_mensagens.insert(tk.END, f"{cantor} | {musica}")

    def remover_pedido_nuvem(self):
        selecao = self.lista_mensagens.curselection()
        if not selecao: 
            return
        idx = selecao[0]
        pedido = self.pedidos_nuvem_cache[idx]
        threading.Thread(target=lambda: requests.delete(f"https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos/{pedido['id']}.json"), daemon=True).start()
        self.lista_mensagens.delete(idx)
        self.pedidos_nuvem_cache.pop(idx)

    def acao_adicionar_pedido_nuvem(self, event=None):
        selecao = self.lista_mensagens.curselection()
        if not selecao:
            return
        
        idx = selecao[0]
        pedido = self.pedidos_nuvem_cache[idx]
        
        opcoes = self.procurar_arquivo_musica_direto(pedido['musica'])
        if opcoes:
            self.finalizar_adicao(pedido['cantor'], opcoes[0])
            threading.Thread(target=lambda: requests.delete(f"https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos/{pedido['id']}.json"), daemon=True).start()
            self.lista_mensagens.delete(idx)
            self.pedidos_nuvem_cache.pop(idx)
        else:
            messagebox.showinfo("Busca", f"Nenhuma música encontrada no disco para: '{pedido['musica']}'")

    def procurar_arquivo_musica_direto(self, texto_procurado):
        texto_limpo_input = self.remover_acentos(texto_procurado.strip().lower())
        formats = [".mp4", ".mkv", ".avi", ".wmv", ".mpg", ".mp3"]
        resultados = []
        if not os.path.exists(self.pasta_sistema): 
            return resultados
        
        for raiz, pastas, arquivos in os.walk(self.pasta_sistema):
            for arquivo in arquivos:
                nome_sem_ext, ext = os.path.splitext(arquivo)
                if ext.lower() in formats:
                    nome_normalizado = self.remover_acentos(nome_sem_ext.lower())
                    texto_input_normalizado = self.remover_acentos(texto_limpo_input.lower())
                    
                    if texto_input_normalizado in nome_normalizado or any(p in nome_normalizado for p in texto_input_normalizado.split() if len(p) > 2):
                        resultados.append({"nome": nome_sem_ext, "caminho": os.path.abspath(os.path.join(raiz, arquivo))})
        return resultados

    def finalizar_adicao(self, cantor, musica_info):
        self.playlist.append({"cantor": cantor, "musica": musica_info["nome"], "caminho": musica_info.get("caminho", "NAO_ENCONTRADO")})
        self.salvar_playlist_memoria()
        self.atualizar_listas_interface()

    def remover_acentos(self, texto):
        return "".join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn').lower()

    def atualizar_listas_interface(self):
        self.lista_visual.delete(0, tk.END)
        for index, item in enumerate(self.playlist, start=1):
            self.lista_visual.insert(tk.END, f"{index}. {item['cantor']} - {item['musica']}")
        
        if self.aguardando_contagem:
            return 
        
        self.canvas_logo.delete("texto_fila")
        largura = self.janela_publico.winfo_width()
        altura = self.janela_publico.winfo_height()
        
        centro_x = largura * 0.35 
        y_inicial_linhas = altura * 0.25
        
        if len(self.playlist) > 0:
            # Texto principal "A SEGUIR:" (tamanho 20)
            self.canvas_logo.create_text(centro_x, y_inicial_linhas, text="A SEGUIR:", font=("Arial Black", 20, "bold"), fill="#ffffff", anchor="w", tags="texto_fila")
            y_inicial_linhas += 50 

            # Primeiro cantor da fila com tamanho aumentado em ~30% (tamanho 24) e destaque imediato
            primeiro = self.playlist[0]
            txt_primeiro = f"1. {primeiro['cantor'].upper()} - {primeiro['musica'].upper()[:30]}"
            self.canvas_logo.create_text(centro_x, y_inicial_linhas, text=txt_primeiro, font=("Arial Black", 24, "bold"), fill="#00ffcc", anchor="w", tags="texto_fila")
            y_inicial_linhas += 60

        # Demais cantores da fila (a partir do segundo) com tamanho normal (tamanho 18)
        for i in range(1, min(len(self.playlist), 8)):
            item = self.playlist[i]
            y_pos = y_inicial_linhas + ((i - 1) * 45)
            txt_formatado = f"{i+1}. {item['cantor'].upper()} - {item['musica'].upper()[:30]}"
            self.canvas_logo.create_text(centro_x, y_pos, text=txt_formatado, font=("Arial Black", 18, "bold"), fill="yellow", anchor="w", tags="texto_fila")

    def gerenciar_clique_transicao(self):
        if not self.playlist: 
            return
        self.musica_preparada = self.playlist.pop(0)
        self.salvar_playlist_memoria()
        self.btn_lancar.configure(text="INICIAR CONTAGEM", state="disabled")
        
        self.canvas_logo.delete("texto_fila")
        self.iniciar_ciclo_contagem(3)

    def iniciar_ciclo_contagem(self, numero):
        self.aguardando_contagem = True
        largura = self.janela_publico.winfo_width()
        altura = self.janela_publico.winfo_height()
        
        self.canvas_logo.delete("contagem_gigante")
        
        if numero > 0:
            self.canvas_logo.create_text(largura/2, altura/2, text=str(numero), font=("Arial Black", 200, "bold"), fill="#fff200", tags="contagem_gigante")
            self.root.after(1000, lambda: self.iniciar_ciclo_contagem(numero - 1))
        else:
            self.canvas_logo.create_text(largura/2, altura/2, text="SOLTA A VOZ!", font=("Arial Black", 80, "bold"), fill="#ffffff", tags="contagem_gigante")
            self.falar_em_fio("Solta a voz!", lambda: self.finalizar_contagem_e_abrir())

    def finalizar_contagem_e_abrir(self):
        self.canvas_logo.delete("contagem_gigante")
        self.aguardando_contagem = False
        self.abrir_reprodutor_vlc()
        self.btn_lancar.configure(text="► ANUNCIAR PRÓXIMO CANTOR", state="normal")
        self.atualizar_listas_interface()

    def abrir_reprodutor_vlc(self):
        if not self.musica_preparada:
            return
        caminho = self.musica_preparada["caminho"]
        if caminho == "NAO_ENCONTRADO":
            messagebox.showwarning("Aviso", "Música não encontrada no disco.")
            return
        if not os.path.exists(caminho):
            messagebox.showerror("Erro", f"Ficheiro não existe em: {caminho}")
            return
        caminho_vlc = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
        if os.path.exists(caminho_vlc):
            subprocess.Popen([caminho_vlc, "--fullscreen", "--play-and-exit", caminho])

    def fechar_aplicativo(self): 
        self.salvar_playlist_memoria()
        self.root.destroy()

    def mover_para_cima(self): 
        selecao = self.lista_visual.curselection()
        if selecao and selecao[0] > 0:
            i = selecao[0]
            self.playlist[i], self.playlist[i-1] = self.playlist[i-1], self.playlist[i]
            self.salvar_playlist_memoria()
            self.atualizar_listas_interface()
            self.lista_visual.selection_set(i-1)

    def mover_para_baixo(self): 
        selecao = self.lista_visual.curselection()
        if selecao and selecao[0] < len(self.playlist)-1:
            i = selecao[0]
            self.playlist[i], self.playlist[i+1] = self.playlist[i+1], self.playlist[i]
            self.salvar_playlist_memoria()
            self.atualizar_listas_interface()
            self.lista_visual.selection_set(i+1)

    def remover_musica_selecionada(self): 
        selecao = self.lista_visual.curselection()
        if selecao: 
            self.playlist.pop(selecao[0])
            self.salvar_playlist_memoria()
            self.atualizar_listas_interface()

    def processar_arquivo_arrastado(self, event):
        dados = event.data
        if not dados: 
            return
        caminho_limpo = os.path.normpath(re.findall(r"\{([^}]+)\}|(\S+)", dados)[0][0].replace('"', "").strip())
        if os.path.isfile(caminho_limpo):
            nome_musica = os.path.basename(caminho_limpo)
            nome_cantor = simpledialog.askstring("FF KARAOKE", "Insira o nome do Cantor:")
            if not nome_cantor: 
                return
            self.playlist.append({"cantor": nome_cantor, "musica": nome_musica, "caminho": caminho_limpo})
            self.salvar_playlist_memoria()
            self.atualizar_listas_interface()

    def adicionar_musica_manual(self):
        c = self.entry_cantor.get().strip()
        m = self.entry_musica.get().strip()
        if not c or not m: 
            return
        opcoes = self.procurar_arquivo_musica_direto(m)
        if opcoes: 
            self.finalizar_adicao(c, opcoes[0])
        else: 
            messagebox.showinfo("Busca", "Nenhuma música encontrada.")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = FFKaraokeApp(root)
    root.mainloop()
