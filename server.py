import streamlit as st
import requests
import json
import os

# --- CONFIGURAÇÕES ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"

st.set_page_config(page_title="FF KARAOKE CLOUD", layout="wide")

# --- CSS PERSONALIZADO ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #D4AF37; }
    h1, h2, h3 { color: #D4AF37 !important; text-align: center; }
    label { color: white !important; font-weight: bold; }
    
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background-color: #1a1a1a !important; 
        border: 2px solid #D4AF37 !important;
        color: #D4AF37 !important;
        border-radius: 8px !important;
    }
    
    div.stButton > button {
        background-color: #D4AF37 !important;
        color: #000 !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        width: 100%;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- CABEÇALHO ---
# Verificação de segurança para a imagem
if os.path.exists("logoweb.png"):
    st.image("logoweb.png", use_container_width=True)
else:
    st.title("🎤 GRUPO FF KARAOKE")

st.markdown("<h4 style='text-align: center; color: #D4AF37;'>INSTAGRAM: ff_karaoke | TIK TOK: ff.karaoke</h4>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: #D4AF37;'>REALIZA A SUA FESTA DE KARAOKE <br> LIGUE : 921204050 / 955099159</h5>", unsafe_allow_html=True)

# --- LÓGICA DE CARGA ---
@st.cache_data(ttl=300)
def carregar_catalogo():
    try:
        resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
        data = resp.json()
        return list(data.keys()) if isinstance(data, dict) else data
    except: return ["Paulo Flores - Garina", "Fausto Fortes - Vou Cantar"]

catalogo_musicas = carregar_catalogo()

# --- LAYOUT EM COLUNAS ---
col_esq, col_dir = st.columns([2, 1])

with col_esq:
    cantor = st.text_input("NOME", placeholder="Escreva o seu nome...")
    busca_musica = st.text_input("PESQUISAR", placeholder="Digite o nome da música...")
    
    musica_final = ""
    if busca_musica:
        resultados = [m for m in catalogo_musicas if busca_musica.lower() in m.lower()]
        if resultados:
            musica_final = st.selectbox("Selecione a música:", resultados)
        else:
            st.warning("Música não encontrada no catálogo.")
            musica_final = st.text_input("Confirmar Pedido Manual:", value=busca_musica)
    
    btn_enviar = st.button("ENVIAR PEDIDO")

with col_dir:
    st.subheader("Tirar Foto")
    foto_selfie = st.camera_input("")

# --- PROCESSAMENTO DO ENVIO ---
if btn_enviar:
    if not cantor or not musica_final:
        st.error("Por favor, preencha o seu nome e selecione a música.")
    else:
        dados = {"cantor": cantor, "musica": musica_final, "tem_foto": True if foto_selfie else False}
        try:
            requests.post(URL_FIREBASE_PEDIDOS, data=json.dumps(dados), timeout=5)
            st.success(f"🎉 Pedido de {musica_final} enviado!")
            st.balloons()
        except Exception as e:
            st.error(f"Erro ao enviar: {e}")
