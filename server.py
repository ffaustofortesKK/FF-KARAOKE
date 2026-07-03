import streamlit as st
import requests

# --- CONFIGURAÇÕES ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"

st.set_page_config(page_title="FF KARAOKE CLOUD", layout="wide")

# --- CSS PERSONALIZADO ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%); color: white; }
    
    /* Redução dos campos para 50% de largura (até o risco vermelho) */
    div[data-baseweb="input"], div[data-baseweb="select"] { width: 50% !important; }
    
    /* Input com texto preto */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important; 
        color: #000000 !important;
        height: 40px !important;
    }
    
    /* Aumentar o retângulo de seleção para ler o texto da música */
    div[data-baseweb="select"] { height: 60px !important; }
    
    /* Botões com fundo amarelo */
    div.stButton > button { 
        background-color: #FFD700 !important; 
        color: #000000 !important; 
        font-weight: bold; 
    }
    
    .welcome-text { color: #FFD700 !important; font-weight: bold; font-size: 24px; }
    </style>
""", unsafe_allow_html=True)

# --- LÓGICA ---
if 'registado' not in st.session_state: st.session_state.registado = False

# Logotipo
st.markdown('<div style="display:flex; justify-content:center;"><img src="https://cdn.phototourl.com/free/2026-07-03-793a0f18-6143-44c8-b56e-e44af828c30c.png" width="300"></div>', unsafe_allow_html=True)

if not st.session_state.registado:
    nome = st.text_input("Nome:")
    st.markdown("[👉 TikTok](https://www.tiktok.com/@ff_karaoke) | [👉 Instagram](https://www.instagram.com/ff.karaoke/)")
    check_social = st.checkbox("Confirmo que segui o Grupo FF nas Redes Sociais")
    if st.button("Concluir Registo"):
        if nome and check_social:
            st.session_state.nome = nome
            st.session_state.registado = True
            st.rerun()
else:
    st.markdown(f'<p class="welcome-text">Bem-vindo, {st.session_state.nome}!</p>', unsafe_allow_html=True)
    busca = st.text_input("Título / Cantor:")
    
    if st.button("Pesquisar"):
        try:
            resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
            cat = list(resp.json().keys()) if isinstance(resp.json(), dict) else resp.json()
            st.session_state.resultados = [m for m in cat if busca.lower() in m.lower()]
            st.rerun()
        except: st.error("Erro na ligação.")

    if 'resultados' in st.session_state and st.session_state.resultados:
        escolha = st.selectbox("Selecione a música:", st.session_state.resultados)
        if st.button("Confirmar Pedido"):
            requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": escolha})
            st.success("👏 Seu pedido foi enviado!")
            st.balloons()
            st.session_state.resultados = None
            st.rerun()
