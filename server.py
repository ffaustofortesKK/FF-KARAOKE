import streamlit as str
import os
from datetime import datetime

# Configuração da página do telemóvel do cliente
str.set_page_config(page_title="FF KARAOKE - Pedir Música", page_icon="🎤", layout="centered")

# Estilo visual personalizado (Cores do FF Karaoke)
str.markdown("""
    <style>
    .main { background-color: #111111; color: white; }
    h1 { color: #f1c40f; text-align: center; font-family: 'Arial', sans-serif; }
    .stButton>button { background-color: #f1c40f; color: black; font-weight: bold; width: 100%; }
    .stButton>button:hover { background-color: #fff200; color: black; }
    </style>
""", unsafe_allow_html=True)

# Título do Aplicativo Web que o cliente vai ver no smartphone
str.markdown("<h1>🎤 FF KARAOKE CLOUD 🎵</h1>", unsafe_allow_html=True)
str.write("---")
str.write("Olá! Escolha a sua música e envie o pedido diretamente para o painel do DJ.")

# Formulário de pedido
with str.form(key="form_pedido"):
    nome_cantor = str.text_input("Seu Nome (Quem vai cantar):", placeholder="Ex: Fausto Fortes")
    nome_musica = str.text_input("Nome da Música ou Artista:", placeholder="Ex: Vou Cantar Para Não Chorar")
    
    botao_enviar = str.form_submit_button(label="🚀 ENVIAR PEDIDO DE MÚSICA")

# Caminho onde o ficheiro de pedidos vai ser guardado temporariamente na nuvem
# Para o teste inicial no Streamlit Cloud, ele cria o ficheiro local na nuvem
ARQUIVO_PEDIDOS = "pedidos.txt"

if botao_enviar:
    if nome_cantor.strip() == "" or nome_musica.strip() == "":
        str.error("❌ Por favor, preencha o seu nome e o nome da música!")
    else:
        # Formata a mensagem exatamente como o teu painel azul espera receber
        linha_pedido = f"{nome_cantor.strip()} || {nome_musica.strip()}\n"
        
        try:
            # Escreve o pedido no arquivo de texto
            with open(ARQUIVO_PEDIDOS, "a", encoding="utf-8") as f:
                f.write(linha_pedido)
                
            str.success(f"✅ Sucesso, {nome_cantor}! O teu pedido de '{nome_musica}' foi enviado. Fica atento à TV para ver a tua vez!")
            str.balloons()  # Efeito visual de celebração na tela do telemóvel
        except Exception as e:
            str.error("Ocorreu um erro ao enviar o pedido. Tente novamente.")
