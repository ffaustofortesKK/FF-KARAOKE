import streamlit as str
import requests

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

str.markdown("<h1>🎤 FF KARAOKE CLOUD 🎵</h1>", unsafe_allow_html=True)
str.write("---")
str.write("Olá! Escolha a sua música e envie o pedido diretamente para o painel do DJ.")

with str.form(key="form_pedido"):
    nome_cantor = str.text_input("Seu Nome (Quem vai cantar):", placeholder="Ex: Fausto Fortes")
    nome_musica = str.text_input("Nome da Música ou Artista:", placeholder="Ex: Vou Cantar Para Não Chorar")
    botao_enviar = str.form_submit_button(label="🚀 ENVIAR PEDIDO DE MÚSICA")

if botao_enviar:
    if nome_cantor.strip() == "" or nome_musica.strip() == "":
        str.error("❌ Por favor, preencha o seu nome e o nome da música!")
    else:
        # Formata o pedido com a separação que o computador espera
        dados_pedido = f"{nome_cantor.strip()} || {nome_musica.strip()}"
        
        try:
            # Envia para a ponte estável na nuvem (usando text/plain para evitar erros de formato)
            url_ponte = "https://kvdb.io/6WbYg7q2Yn6XmZ8pQ7uR5a/ff_pedidos"
            headers = {'Content-Type': 'text/plain'}
            resposta = requests.post(url_ponte, data=dados_pedido.encode('utf-8'), headers=headers, timeout=10)
            
            if resposta.status_code in [200, 201]:
                str.success(f"✅ Sucesso, {nome_cantor}! O teu pedido foi enviado para o DJ.")
                str.balloons()
            else:
                str.error(f"Erro no servidor: {resposta.status_code}. Tenta novamente.")
        except Exception as e:
            str.error("Erro de ligação. Garanta que o telemóvel tem internet ativa.")
