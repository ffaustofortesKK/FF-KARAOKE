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
    /* Fundo com Estrelas */
    .stApp { background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%); }
    
    /* Ajuste do tamanho dos retângulos (Inputs e Selects) */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        padding: 5px !important;
        height: 40px !important;
        background-color: #f0f0f0 !important; /* Fundo claro */
        border: 2px solid #D4AF37 !important;
        border-radius: 5px !important;
    }
    /* Cor do texto dentro dos retângulos: PRETO */
    input, div[data-baseweb="select"] { color: black !important; font-weight: bold; }
    
    /* Logótipo */
    .logo-container { width: 100%; display: flex; justify-content: center; margin-bottom: 10px; }
    .logo-container img { width: 100% !important; max-width: 300px; height: auto !important; object-fit: contain; }
    
    /* Textos brancos com sombra */
    .stApp, label, p, .stCheckbox { color: white !important; text-shadow: 1px 1px 2px #000; }
    
    /* Animação das 6 Estrelas Cadentes */
    .star { position: absolute; width: 2px; height: 2px; background: white; opacity: 0; }
    @keyframes shoot { 0% { transform: translate(0, 0); opacity: 1; } 100% { transform: translate(600px, 600px); opacity: 0; } }
    
    /* Criação das 6 estrelas com delays diferentes */
    .s1 { animation: shoot 4s linear infinite; top: 10%; left: 5%; }
    .s2 { animation: shoot 4s linear infinite 0.5s; top: 20%; left: 10%; }
    .s3 { animation: shoot 4s linear infinite 1s; top: 5%; left: 20%; }
    .s4 { animation: shoot 4s linear infinite 1.5s; top: 15%; left: 30%; }
    .s5 { animation: shoot 4s linear infinite 2s; top: 25%; left: 5%; }
    .s6 { animation: shoot 4s linear infinite 2.5s; top: 30%; left: 15%; }
    </style>
""", unsafe_allow_html=True)

# Inserção das estrelas cadentes no HTML
st.markdown('<div class="star s1"></div><div class="star s2"></div><div class="star s3"></div><div class="star s4"></div><div class="star s5"></div><div class="star s6"></div>', unsafe_allow_html=True)

if 'registado' not in st.session_state: st.session_state.registado = False

# --- CABEÇALHO ---
st.markdown('<div class="logo-container"><img src="https://cdn.phototourl.com/free/2026-07-03-793a0f18-6143-44c8-b56e-e44af828c30c.png"></div>', unsafe_allow_html=True)

# --- FASE 1: REGISTO ---
if not st.session_state.registado:
    nome = st.text_input("Nome:")
    st.markdown("[👉 Seguir no TikTok](https://www.tiktok.com/@ff_karaoke) | [👉 Seguir no Instagram](https://www.instagram.com/ff.karaoke/)")
    check_social = st.checkbox("Confirmo que segui o Grupo FF nas Redes Sociais")
    if st.button("Concluir Registo"):
        if nome and check_social:
            st.session_state.nome = nome
            st.session_state.registado = True
            st.rerun()
else:
    st.markdown(f'<p style="color: #FFD700; font-weight: bold; font-size: 24px;">Bem-vindo, {st.session_state.nome}!</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        busca = st.text_input("Título / Cantor:")
        if st.button("Pesquisar"):
            try:
                resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
                cat = list(resp.json().keys()) if isinstance(resp.json(), dict) else resp.json()
                st.session_state.resultados_busca = [m for m in cat if busca.lower() in m.lower()]
                st.rerun()
            except: st.error("Erro na busca.")

        if 'resultados_busca' in st.session_state and st.session_state.resultados_busca:
            escolha = st.selectbox("Selecione:", st.session_state.resultados_busca)
            if st.button("Confirmar Pedido"):
                requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": escolha})
                st.success("👏 Seu pedido foi enviado!")
                st.balloons()
                st.session_state.resultados_busca = None
                st.rerun()

    with col2:
        st.camera_input("Foto")
        if st.button("Sair"):
            st.session_state.registado = False
            st.rerun()
