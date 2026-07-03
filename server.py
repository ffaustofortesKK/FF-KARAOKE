import streamlit as st
import requests
import json

# --- CONFIGURAÇÕES ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"

st.set_page_config(page_title="FF KARAOKE CLOUD", layout="wide")

# --- CSS PERSONALIZADO ---
st.markdown("""
    <style>
    /* Fundo preto com estrelas */
    .stApp { background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%); color: white; }
    
    /* Logótipo Completo */
    .logo-container { width: 100%; display: flex; justify-content: center; margin-bottom: 20px; }
    .logo-container img { width: 100% !important; max-width: 300px; height: auto !important; object-fit: contain; }
    
    /* Cores de texto brancas */
    label { color: white !important; font-weight: bold; }
    
    /* Campos de Input reduzidos a 50% e texto preto */
    div[data-baseweb="input"], div[data-baseweb="select"] { width: 50% !important; }
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important; 
        color: #000000 !important;
        border: 2px solid #D4AF37 !important;
        height: 40px !important;
    }
    input { color: #000000 !important; font-weight: bold; }
    
    /* Botões Amarelos */
    div.stButton > button { background-color: #FFD700 !important; color: #000000 !important; font-weight: bold; }
    
    /* Caixa de Sucesso */
    .success-box { background-color: #008000; color: #FFFFFF; padding: 10px; border-radius: 5px; font-weight: bold; margin-top: 10px; width: 50%; }
    </style>
""", unsafe_allow_html=True)

if 'registado' not in st.session_state: st.session_state.registado = False
if 'resultados' not in st.session_state: st.session_state.resultados = None

# Cabeçalho
st.markdown('<div class="logo-container"><img src="https://cdn.phototourl.com/free/2026-07-03-793a0f18-6143-44c8-b56e-e44af828c30c.png"></div>', unsafe_allow_html=True)

if not st.session_state.registado:
    st.subheader("📝 Registo Inicial")
    nome = st.text_input("Nome:")
    st.markdown("[👉 TikTok](https://www.tiktok.com/@ff_karaoke) | [👉 Instagram](https://www.instagram.com/ff.karaoke/)")
    check_social = st.checkbox("Confirmo que segui o Grupo FF nas Redes Sociais")
    if st.button("Concluir Registo"):
        if nome and check_social:
            st.session_state.nome = nome
            st.session_state.registado = True
            st.rerun()
else:
    st.markdown(f'<p style="color:#FFD700; font-weight:bold; font-size:24px;">Bem-vindo, {st.session_state.nome}!</p>', unsafe_allow_html=True)
    
    busca = st.text_input("Título / Cantor:")
    if st.button("Pesquisar"):
        try:
            resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
            dados = resp.json()
            cat = list(dados.keys()) if isinstance(dados, dict) else dados
            st.session_state.resultados = [m for m in cat if busca.lower() in m.lower()]
            st.rerun()
        except:
            pass

    if st.session_state.resultados:
        escolha = st.selectbox("Selecione a música:", st.session_state.resultados)
        if st.button("Confirmar Pedido"):
            requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": escolha})
            st.markdown('<div class="success-box">o seu pedido foi enviado com sucesso</div>', unsafe_allow_html=True)
            st.balloons()
            st.session_state.resultados = None
