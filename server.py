import streamlit as st
import requests
import base64
from io import BytesIO

# --- CONFIGURAÇÕES ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"
LINK_LOGO = "https://cdn.phototourl.com/free/2026-07-03-793a0f18-6143-44c8-b56e-e44af828c30c.png"

st.set_page_config(page_title="FF KARAOKE CLOUD", layout="wide")

# CSS personalizado para o Logotipo no fundo
# O linear-gradient escurece a imagem para que o texto branco seja legível
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(9, 10, 15, 0.8), rgba(9, 10, 15, 0.8)), url('{LINK_LOGO}');
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
""", unsafe_allow_html=True)

if 'registado' not in st.session_state: st.session_state.registado = False

if not st.session_state.registado:
    st.subheader("📝 Registo Inicial")
    nome = st.text_input("Nome:")
    if st.button("Concluir Registo"):
        if nome:
            st.session_state.nome = nome
            st.session_state.registado = True
            st.rerun()
else:
    # --- LAYOUT: CAMARA NO TOPO ESQUERDO ---
    col_cam, col_main = st.columns([1, 2])
    
    with col_cam:
        st.subheader("📸 Sua Foto")
        foto_capturada = st.camera_input("Tirar foto para o pedido")
        if foto_capturada:
            # Converte a foto para base64 para enviar via JSON
            bytes_data = foto_capturada.getvalue()
            st.session_state.foto_b64 = base64.b64encode(bytes_data).decode()
        else:
            st.session_state.foto_b64 = None

    with col_main:
        st.title(f"Bem-vindo, {st.session_state.nome}!")
        
        # BUSCA
        busca = st.text_input("Pesquisar Música:")
        if busca:
            try:
                resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
                dados = resp.json()
                cat = list(dados.keys()) if isinstance(dados, dict) else dados
                resultados = [m for m in cat if busca.lower() in m.lower()]
                escolha = st.selectbox("Selecione:", resultados)
            except: escolha = None
        else: escolha = None

        # --- ENVIO COM OPÇÃO DE FOTO ---
        if escolha:
            st.write(f"Música selecionada: **{escolha}**")
            enviar_com_foto = st.radio("Deseja enviar seu pedido com esta foto?", ["Não", "Sim"])
            
            if st.button("Confirmar Pedido"):
                payload = {
                    "cantor": st.session_state.nome, 
                    "musica": escolha,
                    "foto": st.session_state.foto_b64 if (enviar_com_foto == "Sim" and st.session_state.foto_b64) else None
                }
                requests.post(URL_FIREBASE_PEDIDOS, json=payload)
                st.success("Pedido enviado com sucesso!")
                st.balloons()

    if st.button("Sair"):
        st.session_state.registado = False
        st.rerun()
