import streamlit as st
import requests
import json

# --- CONFIGURAÇÕES ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"

st.set_page_config(page_title="FF KARAOKE CLOUD", layout="wide")

# --- CSS E ANIMAÇÕES ---
st.markdown("""
    <style>
    /* Animação de Fundo com Estrelas */
    .stApp {
        background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%);
        background-color: #000;
        overflow: hidden;
    }
    
    /* Estrelas Cintilantes (Efeito de pontos) */
    body::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: url('https://www.transparenttextures.com/patterns/stardust.png');
        z-index: -1; animation: twinkle 5s infinite;
    }
    
    @keyframes twinkle { 0%, 100% { opacity: 0.5; } 50% { opacity: 1; } }

    /* Estrela Cadente */
    .shooting-star {
        position: absolute; width: 2px; height: 2px; background: white;
        animation: shoot 3s linear infinite; opacity: 0;
    }
    @keyframes shoot { 0% { transform: translateX(0) translateY(0); opacity: 1; } 100% { transform: translateX(500px) translateY(500px); opacity: 0; } }

    /* Estilização Geral */
    .logo-container { width: 100%; display: flex; justify-content: center; margin-bottom: 20px; }
    .logo-container img { width: 100% !important; max-width: 400px; height: auto !important; object-fit: contain; }
    
    /* Texto branco com sombra */
    .stApp, label, p, div, .stCheckbox { color: white !important; text-shadow: 1px 1px 4px #000; }
    
    /* Inputs: Branco com Sombra */
    input, div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.1) !important; 
        border: 2px solid #D4AF37 !important;
        color: white !important; 
        text-shadow: 1px 1px 2px #000;
    }
    
    .welcome-text { color: #FFD700 !important; font-weight: bold; font-size: 28px !important; text-shadow: 2px 2px 4px #000; }
    div.stButton > button { background-color: #D4AF37 !important; color: #000 !important; font-weight: bold; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# Estrela cadente passando
st.markdown('<div class="shooting-star" style="top:10%; left:10%;"></div>', unsafe_allow_html=True)

if 'registado' not in st.session_state: st.session_state.registado = False
if 'resultados_busca' not in st.session_state: st.session_state.resultados_busca = None

st.markdown('<div class="logo-container"><img src="https://cdn.phototourl.com/free/2026-07-03-793a0f18-6143-44c8-b56e-e44af828c30c.png"></div>', unsafe_allow_html=True)

if not st.session_state.registado:
    st.subheader("📝 Registo Inicial")
    nome = st.text_input("Nome:")
    check_social = st.checkbox("Confirmo que segui o Grupo FF nas Redes Sociais")
    if st.button("Concluir Registo"):
        if nome and check_social:
            st.session_state.nome = nome
            st.session_state.registado = True
            st.rerun()
else:
    st.markdown(f'<p class="welcome-text">Bem-vindo, {st.session_state.nome}!</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        busca = st.text_input("Título / Cantor:")
        if st.button("Pesquisar na Nuvem"):
            try:
                resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
                cat = list(resp.json().keys()) if isinstance(resp.json(), dict) else resp.json()
                st.session_state.resultados_busca = [m for m in cat if busca.lower() in m.lower()]
                st.rerun()
            except: st.error("Erro de conexão.")

        if st.session_state.resultados_busca:
            escolha = st.selectbox("Selecione a música:", st.session_state.resultados_busca)
            if st.button("Confirmar Pedido"):
                requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": escolha})
                # Efeito de aplausos e mensagem
                st.success("👏 Seu pedido foi enviado! 👏")
                st.balloons()
                st.session_state.resultados_busca = None
                st.rerun()

    with col2:
        st.camera_input("Foto")
        if st.button("Sair"):
            st.session_state.registado = False
            st.rerun()
