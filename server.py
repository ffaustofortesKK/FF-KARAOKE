import streamlit as st
import requests
import json
import time

# Configuração da página
st.set_page_config(page_title="FF KARAOKE CLOUD", layout="wide")

# Carregar o CSS externo
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# --- LÓGICA DO APP ---
st.title("GRUPO FF KARAOKE")
st.markdown("<h4 style='text-align: center; color: #D4AF37;'>INSTAGRAM: ff_karaoke | TIK TOK: ff.karaoke</h4>", unsafe_allow_html=True)
st.write("---")

col1, col2 = st.columns([2, 1])

# Carregar catálogo
URL_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"
try:
    resp = requests.get(URL_CATALOGO, timeout=5)
    catalogo = resp.json() if resp.status_code == 200 else {}
except: catalogo = {}

opcoes = list(catalogo.keys()) if isinstance(catalogo, dict) else []

with col1:
    nome = st.text_input("nome")
    musica = st.selectbox("pesquisar Musica", ["-- Selecione --"] + opcoes)
    
    if st.button("enviar"):
        if nome and musica != "-- Selecione --":
            # Aqui vai o código de envio para o Firebase
            st.success("Pedido enviado com sucesso!")
        else:
            st.error("Por favor, preencha o nome e escolha a música.")

with col2:
    st.subheader("tirar Foto")
    foto = st.camera_input("")
    if foto:
        st.write("Foto capturada!")

st.write("---")
st.subheader("📺 Fila de Espera")
