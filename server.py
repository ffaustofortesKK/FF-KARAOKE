import streamlit as st
import requests
import json

# --- CONFIGURAÇÕES ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"

st.set_page_config(page_title="FF KARAOKE CLOUD", layout="wide")

# --- CSS PARA O TEMA DOURADO E PRETO ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #D4AF37; }
    h1, h2, h3 { color: #D4AF37 !important; text-align: center; }
    
    /* Inputs personalizados */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background-color: #1a1a1a !important; 
        border: 2px solid #D4AF37 !important;
        color: #D4AF37 !important;
        border-radius: 8px !important;
    }
    
    /* Botão Enviar estilo Dourado */
    div.stButton > button {
        background-color: #D4AF37 !important;
        color: #000 !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# --- CABEÇALHO ---
st.title("🎤 GRUPO FF KARAOKE")
st.markdown("<h4 style='text-align: center; color: #D4AF37;'>INSTAGRAM: ff_karaoke | TIK TOK: ff.karaoke</h4>", unsafe_allow_html=True)

# --- LÓGICA DE CARGA ---
@st.cache_data(ttl=300)
def carregar_catalogo():
    try:
        resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
        return resp.json() if resp.status_code == 200 else []
    except: return ["Paulo Flores - Garina", "Fausto Fortes - Vou Cantar"]

catalogo_musicas = carregar_catalogo()

# --- LAYOUT EM COLUNAS (Esquerda: Formulário, Direita: Foto) ---
col_esq, col_dir = st.columns([2, 1])

with col_esq:
    cantor = st.text_input("Nome", placeholder="Escreva o seu nome...")
    busca_musica = st.text_input("Pesquisar Música", placeholder="Ex: Paulo Flores").strip()
    
    musica_final = ""
    if busca_musica:
        resultados = [m for m in catalogo_musicas if busca_musica.lower() in m.lower()]
        if resultados:
            musica_final = st.selectbox("Escolha a música:", resultados)
        else:
            musica_final = st.text_input("Pedido Manual:", value=busca_musica)
    
    btn_enviar = st.button("ENVIAR PEDIDO", use_container_width=True)

with col_dir:
    st.subheader("Tirar Foto")
    foto_selfie = st.camera_input("")

# --- PROCESSAMENTO DO ENVIO ---
if btn_enviar:
    if not cantor or not musica_final:
        st.error("Preencha nome e música!")
    else:
        dados = {"cantor": cantor, "musica": musica_final, "tem_foto": True if foto_selfie else False}
        try:
            requests.post(URL_FIREBASE_PEDIDOS, data=json.dumps(dados), timeout=5)
            st.success(f"Pedido de {musica_final} enviado!")
        except Exception as e:
            st.error(f"Erro: {e}")
