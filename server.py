import streamlit as st
import requests

# Link oficial do teu Firebase
URL_FIREBASE = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedido.json"

# Configuração da página do Cliente
st.set_page_config(page_title="FF KARAOKE - Pedir Música", page_icon="🎤", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #111111; color: white; }
    h1 { color: #f1c40f; text-align: center; font-family: 'Arial', sans-serif; }
    .stButton>button { background-color: #f1c40f; color: black; font-weight: bold; width: 100%; height: 3em; border-radius: 10px; }
    .stButton>button:hover { background-color: #fff200; color: black; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🎤 FF KARAOKE CLOUD 🎵</h1>", unsafe_allow_html=True)
st.write("---")

# Formulário de envio para o cliente
with st.form(key="form_pedido", clear_on_submit=True):
    nome_cantor = st.text_input("Seu Nome (Quem vai cantar):", placeholder="Ex: Fausto Fortes")
    nome_musica = st.text_input("Nome da Música ou Artista:", placeholder="Ex: Melodia")
    botao_enviar = st.form_submit_button(label="🚀 ENVIAR PEDIDO DE MÚSICA")

if botao_enviar:
    if nome_cantor.strip() == "" or nome_musica.strip() == "":
        st.error("❌ Por favor, preencha o seu nome e o nome da música!")
    else:
        try:
            dados = {
                "cantor": nome_cantor.strip(),
                "musica": nome_musica.strip()
            }
            # Envia os dados diretamente para o Firebase usando PUT (substitui o último)
            resposta = requests.put(URL_FIREBASE, json=dados, timeout=5)
            
            if resposta.status_code == 200:
                st.success(f"✅ Sucesso, {nome_cantor}! O teu pedido foi enviado.")
                st.balloons()
            else:
                st.error(f"Erro no servidor externo: Status {resposta.status_code}")
        except Exception as e:
            st.error(f"Erro ao enviar o pedido: {e}")
