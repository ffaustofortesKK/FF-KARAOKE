import streamlit as st
import requests
import json
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="FF KARAOKE CLOUD", layout="wide")

# --- CSS PARA O TEMA PREMIUM ---
st.markdown("""
    <style>
    /* Fundo escuro e fonte dourada */
    .stApp {
        background-color: #000000;
        color: #D4AF37;
    }
    /* Estilo dos campos */
    input, .stSelectbox > div {
        background-color: #1a1a1a !important;
        border: 2px solid #D4AF37 !important;
        color: #D4AF37 !important;
        border-radius: 5px !important;
    }
    /* Estilo do Botão */
    .stButton > button {
        background-color: #D4AF37 !important;
        color: #000 !important;
        font-weight: bold !important;
        border-radius: 5px !important;
        width: 100%;
        margin-top: 20px;
    }
    /* Títulos */
    h1, h2, h3 { color: #D4AF37 !important; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- CABEÇALHO ---
st.title("GRUPO FF KARAOKE")
st.markdown("<h4 style='text-align: center;'>INSTAGRAM: ff_karaoke | TIK TOK: ff.karaoke</h4>", unsafe_allow_html=True)
st.write("---")

# --- LAYOUT PRINCIPAL ---
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
            pedido = {"cantor": nome, "musica": musica, "timestamp": time.time()}
            # Enviar para Firebase (substitui pela tua URL de pedidos)
            # requests.post("...", json=pedido) 
            st.success("Pedido enviado!")
        else:
            st.error("Preencha o nome e escolha a música.")

with col2:
    st.subheader("tirar Foto")
    # Este componente cria exatamente o retângulo para a selfie
    foto = st.camera_input("") 
    if foto:
        st.write("Foto capturada!")

# --- RODAPÉ ---
st.write("---")
st.subheader("📺 Fila de Espera")
# Aqui podes adicionar o código para mostrar os pedidos (Segunda Tela)
