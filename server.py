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
    .stApp { background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%); color: white; }
    
    /* Logótipo */
    .logo-container { width: 100%; display: flex; justify-content: center; }
    .logo-container img { width: 100% !important; max-width: 300px; height: auto !important; object-fit: contain; }
    
    /* Campos de Input e Select - Tamanho reduzido e texto preto */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important; 
        color: #000000 !important;
        border: 1px solid #D4AF37 !important;
        height: 35px !important; /* Altura reduzida */
        padding: 5px !important;
    }
    input { color: #000000 !important; font-weight: bold; }

    /* Estrelas Cadentes */
    .star { position: absolute; width: 2px; height: 2px; background: white; opacity: 0; animation: shoot 5s linear infinite; }
    @keyframes shoot { 0% { transform: translate(0, 0); opacity: 1; } 100% { transform: translate(800px, 800px); opacity: 0; } }
    
    .welcome-text { color: #FFD700 !important; font-weight: bold; font-size: 24px; text-shadow: 2px 2px 4px #000; }
    </style>
""", unsafe_allow_html=True)

# Criar 6 estrelas cadentes com posições diferentes
for i in range(6):
    st.markdown(f'<div class="star" style="top:{i*15}%; left:{i*10}%; animation-delay:{i}s;"></div>', unsafe_allow_html=True)

# --- LÓGICA ---
if 'registado' not in st.session_state: st.session_state.registado = False

st.markdown('<div class="logo-container"><img src="https://cdn.phototourl.com/free/2026-07-03-793a0f18-6143-44c8-b56e-e44af828c30c.png"></div>', unsafe_allow_html=True)

if not st.session_state.registado:
    st.subheader("📝 Registo Inicial")
    nome = st.text_input("Nome:")
    # Reintroduzidos os links
    st.markdown("[👉 TikTok](https://www.tiktok.com/@ff_karaoke) | [👉 Instagram](https://www.instagram.com/ff.karaoke/)")
    check_social = st.checkbox("Confirmo que segui o Grupo FF nas Redes Sociais")
    if st.button("Concluir Registo"):
        if nome and check_social:
            st.session_state.nome = nome
            st.session_state.registado = True
            st.rerun()
else:
    st.markdown(f'<p class="welcome-text">Bem-vindo, {st.session_state.nome}!</p>', unsafe_allow_html=True)
    busca = st.text_input("Pesquisar música:")
    
    if st.button("Pesquisar"):
        try:
            resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
            cat = list(resp.json().keys()) if isinstance(resp.json(), dict) else resp.json()
            st.session_state.resultados = [m for m in cat if busca.lower() in m.lower()]
            st.rerun()
        except: st.error("Erro na ligação.")

    if 'resultados' in st.session_state and st.session_state.resultados:
        escolha = st.selectbox("Selecione:", st.session_state.resultados)
        if st.button("Confirmar Pedido"):
            requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": escolha})
            st.success("👏 Seu pedido foi enviado!")
            st.balloons()
            st.session_state.resultados = None
            st.rerun()
