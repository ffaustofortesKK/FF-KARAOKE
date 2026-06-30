import streamlit as st
import requests
import json

# --- CONFIGURAÇÕES ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"

st.set_page_config(page_title="FF KARAOKE CLOUD", layout="wide")

# --- LÓGICA DE ESTADO (Nome e Tema) ---
if 'nome_cantor' not in st.session_state:
    st.session_state.nome_cantor = ""
if 'tema' not in st.session_state:
    st.session_state.tema = "Preto"

# --- CSS DINÂMICO ---
cor_bg = "#000000" if st.session_state.tema == "Preto" else "#FFFFFF"
cor_texto = "#D4AF37" if st.session_state.tema == "Preto" else "#000000"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {cor_bg}; color: {cor_texto}; }}
    h1, h2, h3 {{ color: {cor_texto} !important; text-align: center; }}
    label, .stTextInput > div > div > input {{ 
        color: {cor_texto} !important; 
        font-weight: bold !important; 
        text-shadow: 1px 1px 2px #888;
    }}
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {{
        background-color: #222 !important; 
        border: 2px solid {cor_texto} !important;
        border-radius: 8px !important;
    }}
    div.stButton > button {{
        background-color: {cor_texto} !important;
        color: {cor_bg} !important;
        font-weight: bold !important;
        width: 100%;
    }}
    </style>
""", unsafe_allow_html=True)

# --- CABEÇALHO ---
st.image("https://i.ibb.co/HfKTnDDQ/logoweb.png", use_container_width=True)
st.markdown(f"<h4 style='text-align: center; color: {cor_texto};'>INSTAGRAM: ff_karaoke | TIK TOK: ff.karaoke</h4>", unsafe_allow_html=True)

# --- OPÇÕES DE TEMA ---
st.session_state.tema = st.radio("Escolha o Tema:", ["Preto", "Branco"], horizontal=True)

# --- LÓGICA DE REGISTO DE NOME ---
if not st.session_state.nome_cantor:
    nome_input = st.text_input("Digite o seu nome para começar:")
    if st.button("Guardar Nome"):
        st.session_state.nome_cantor = nome_input
        st.rerun()
else:
    st.success(f"Olá, {st.session_state.nome_cantor}!")
    if st.button("Trocar Nome / Limpar"):
        st.session_state.nome_cantor = ""
        st.rerun()

    # --- LÓGICA DE PESQUISA (Apenas se o nome estiver definido) ---
    @st.cache_data(ttl=300)
    def carregar_catalogo():
        try:
            resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
            return list(resp.json().keys()) if resp.status_code == 200 else []
        except: return []

    catalogo = carregar_catalogo()
    
    col1, col2 = st.columns([2, 1])
    with col1:
        busca = st.text_input("PESQUISAR MÚSICA:")
        musica_final = ""
        if busca:
            res = [m for m in catalogo if busca.lower() in m.lower()]
            if res:
                musica_final = st.selectbox("Selecione:", res)
            else:
                musica_final = st.text_input("Pedido Manual:", value=busca)
        
        if st.button("ENVIAR PEDIDO"):
            if musica_final:
                dados = {"cantor": st.session_state.nome_cantor, "musica": musica_final}
                requests.post(URL_FIREBASE_PEDIDOS, json=dados)
                st.balloons()
                st.success("Enviado!")

    with col2:
        st.subheader("Foto")
        foto = st.camera_input("")
