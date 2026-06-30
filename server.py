import streamlit as st
import requests
import json
import time

URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedido.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"

st.set_page_config(page_title="FF Karaoke Cloud", layout="wide")

# --- INICIALIZAÇÃO DE SESSÃO ---
if 'nome_cliente' not in st.session_state: st.session_state.nome_cliente = ""
if 'foto_cliente' not in st.session_state: st.session_state.foto_cliente = None

st.title("🎤 FF KARAOKE CLOUD")

# --- PERFIL DO CANTOR ---
with st.sidebar:
    st.header("👤 Perfil do Cantor")
    nome_input = st.text_input("Teu Nome:", value=st.session_state.nome_cliente)
    
    # Self-input para foto (não obrigatório)
    foto_camera = st.camera_input("Tirar Selfie (Opcional)")
    
    if st.button("Guardar Perfil"):
        st.session_state.nome_cliente = nome_input
        if foto_camera: 
            st.session_state.foto_cliente = foto_camera.getvalue()
        st.success("Perfil Guardado!")

# --- ÁREA DO PEDIDO ---
if st.session_state.nome_cliente:
    st.write(f"### Bem-vindo, {st.session_state.nome_cliente}!")
    if st.session_state.foto_cliente:
        st.image(st.session_state.foto_cliente, width=150)
    
    # Leitura segura do catálogo
    try:
        resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
        catalogo = resp.json() if resp.status_code == 200 else {}
    except:
        catalogo = {}

    # Lógica robusta para tratar dicionário ou lista
    if isinstance(catalogo, dict):
        opcoes = list(catalogo.keys())
    else:
        opcoes = catalogo if isinstance(catalogo, list) else []

    with st.form("form_pedido", clear_on_submit=True):
        musica = st.selectbox("Escolha a música:", ["-- Selecione --"] + opcoes)
        btn = st.form_submit_button("🚀 Enviar Pedido")
        
        if btn and musica != "-- Selecione --":
            arquivo = catalogo[musica] if isinstance(catalogo, dict) else musica
            pedido = {
                "cantor": st.session_state.nome_cliente,
                "musica": musica,
                "arquivo_real": arquivo,
                "timestamp": time.time()
            }
            requests.post(URL_FIREBASE_PEDIDOS, json=pedido)
            st.success(f"Pedido de '{musica}' enviado!")

# --- SEGUNDA TELA (ECRÃ DO DJ) ---
st.markdown("---")
st.header("📺 Ecrã do DJ (Próximo Cantor)")

pedidos_raw = requests.get(URL_FIREBASE_PEDIDOS).json() or {}
if pedidos_raw:
    # Transforma o dicionário do Firebase numa lista ordenada pelo timestamp
    lista_pedidos = list(pedidos_raw.values())
    
    for i, p in enumerate(lista_pedidos, 1):
        with st.container():
            col1, col2 = st.columns([1, 6])
            with col1:
                st.subheader(f"#{i}")
            with col2:
                st.write(f"**Cantor:** {p.get('cantor', 'N/A')}")
                st.write(f"**Música:** {p.get('musica', 'N/A')}")
            st.divider()
else:
    st.info("Nenhum pedido na fila.")
