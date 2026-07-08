import streamlit as st
import requests
import base64
from io import BytesIO

# --- CONFIGURAÇÕES ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"
LINK_LOGO = "https://cdn.phototourl.com/free/2026-07-03-793a0f18-6143-44c8-b56e-e44af828c30c.png"

st.set_page_config(page_title="FF KARAOKE CLOUD", layout="wide")

# --- CSS (Mantido igual) ---
st.markdown(f"""
    <style>
    .stApp {{ background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%); color: white; }}
    .success-box {{ background-color: #008000; color: #FFFFFF; padding: 10px; border-radius: 5px; font-weight: bold; width: 40%; }}
    </style>
""", unsafe_allow_html=True)

if 'registado' not in st.session_state: st.session_state.registado = False

# Cabeçalho
st.markdown(f'<div style="display:flex; justify-content:center;"><img src="{LINK_LOGO}" width="150"></div>', unsafe_allow_html=True)

if not st.session_state.registado:
    st.subheader("📝 Registo Inicial")
    nome = st.text_input("Nome:")
    if st.button("Concluir Registo"):
        if nome:
            st.session_state.nome = nome
            st.session_state.registado = True
            st.rerun()
else:
    col_main, col_cam = st.columns([2, 1])
    
    with col_cam:
        # Captura da foto
        foto_capturada = st.camera_input("Tire sua foto")
        st.session_state.foto_base64 = None
        if foto_capturada:
            # Converte a imagem para Base64 para envio JSON
            bytes_data = foto_capturada.getvalue()
            st.session_state.foto_base64 = base64.b64encode(bytes_data).decode('utf-8')

    with col_main:
        with st.form("form_busca", clear_on_submit=True):
            busca = st.text_input("Título / Cantor:")
            if st.form_submit_button("Pesquisar"):
                try:
                    resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
                    dados = resp.json()
                    cat = list(dados.keys()) if isinstance(dados, dict) else dados
                    st.session_state.resultados = [m for m in cat if busca.lower() in m.lower()]
                except: st.error("Erro na busca")
        
        if 'resultados' in st.session_state and st.session_state.resultados:
            escolha = st.selectbox("Selecione:", st.session_state.resultados, key="sel_musica")
            if st.button("Confirmar Pedido"):
                # ENVIO DO PEDIDO COM A FOTO
                payload = {
                    "cantor": st.session_state.nome, 
                    "musica": escolha,
                    "foto": st.session_state.foto_base64 if 'foto_base64' in st.session_state else None
                }
                requests.post(URL_FIREBASE_PEDIDOS, json=payload)
                st.success("Pedido enviado com sucesso!")
                st.session_state.resultados = None
                st.rerun()

    if st.button("Sair"):
        st.session_state.registado = False
        st.rerun()
