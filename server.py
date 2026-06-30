import streamlit as st
import requests
import json
import time

# --- CONFIGURAÇÕES ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedido.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"

st.set_page_config(page_title="FF KARAOKE", layout="wide")

# --- CSS PARA O DESIGN DOURADO (O "LOOK & FEEL" DA IMAGEM) ---
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #D4AF37; }
    h1 { color: #D4AF37; text-align: center; font-family: 'Arial Black'; }
    div.stButton > button { 
        background-color: #D4AF37; color: #000; font-weight: bold; 
        border-radius: 10px; width: 100%; height: 50px; border: none;
    }
    div[data-baseweb="input"], div[data-baseweb="select"] { 
        background-color: #1a1a1a !important; border: 1px solid #D4AF37 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSÃO PARA MANTER DADOS ---
if 'nome_cliente' not in st.session_state: st.session_state.nome_cliente = ""
if 'foto_cliente' not in st.session_state: st.session_state.foto_cliente = None

st.title("GRUPO FF KARAOKE")

# --- LAYOUT (Colunas iguais à imagem) ---
col1, col2 = st.columns([1, 1])

# Lógica do Catálogo
try:
    resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
    catalogo = resp.json() if resp.status_code == 200 else {}
except: catalogo = {}

opcoes = list(catalogo.keys()) if isinstance(catalogo, dict) else []

with col1:
    # Nome
    nome_input = st.text_input("Nome", value=st.session_state.nome_cliente, placeholder="Escreva o seu nome...")
    st.session_state.nome_cliente = nome_input
    
    # Música
    musica = st.selectbox("Localizar musica", ["-- Selecione --"] + opcoes)
    
    # Botão Enviar
    if st.button("ENVIAR PEDIDO"):
        if st.session_state.nome_cliente and musica != "-- Selecione --":
            pedido = {
                "cantor": st.session_state.nome_cliente,
                "musica": musica,
                "arquivo_real": catalogo.get(musica, musica),
                "timestamp": time.time()
            }
            requests.post(URL_FIREBASE_PEDIDOS, json=pedido)
            st.success("Pedido enviado com sucesso!")
        else:
            st.error("Preencha o nome e escolha a música.")

with col2:
    st.write("### Carregar Foto")
    foto_camera = st.camera_input("")
    if foto_camera:
        st.session_state.foto_cliente = foto_camera.getvalue()

# --- ÁREA DO DJ (Segunda Tela) ---
st.markdown("---")
st.subheader("📺 Fila de Espera (Visão do DJ)")
pedidos_raw = requests.get(URL_FIREBASE_PEDIDOS).json() or {}
if pedidos_raw:
    for i, p in enumerate(pedidos_raw.values(), 1):
        st.write(f"**#{i}** - **Cantor:** {p['cantor']} | **Música:** {p['musica']}")
else:
    st.info("Nenhum pedido na fila.")
