import streamlit as st
import requests
import json
import time

# Configurações do Firebase
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedido.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"

st.set_page_config(page_title="FF Karaoke Cloud", layout="wide")

# --- INICIALIZAÇÃO DE SESSÃO ---
if 'nome_cliente' not in st.session_state: st.session_state.nome_cliente = ""
if 'foto_cliente' not in st.session_state: st.session_state.foto_cliente = None

st.title("🎤 FF KARAOKE CLOUD")

# --- LOGIN / PERFIL DO CANTOR ---
with st.sidebar:
    st.header("👤 Perfil do Cantor")
    nome_input = st.text_input("Teu Nome:", value=st.session_state.nome_cliente)
    foto_file = st.file_uploader("Escolher Foto:", type=['jpg', 'png'])
    
    if st.button("Guardar Perfil"):
        st.session_state.nome_cliente = nome_input
        if foto_file: st.session_state.foto_cliente = foto_file.getvalue()
        st.success("Perfil Guardado!")

# --- ÁREA DO PEDIDO ---
if st.session_state.nome_cliente:
    st.write(f"### Bem-vindo, {st.session_state.nome_cliente}!")
    if st.session_state.foto_cliente:
        st.image(st.session_state.foto_cliente, width=100)
    
    catalogo = requests.get(URL_FIREBASE_CATALOGO).json() or {}
    
    with st.form("form_pedido", clear_on_submit=True):
        musica = st.selectbox("Escolha a música:", ["-- Selecione --"] + list(catalogo.keys()))
        btn = st.form_submit_button("🚀 Enviar Pedido")
        
        if btn and musica != "-- Selecione --":
            pedido = {
                "cantor": st.session_state.nome_cliente,
                "musica": musica,
                "arquivo_real": catalogo[musica],
                "timestamp": time.time()
            }
            requests.post(URL_FIREBASE_PEDIDOS, json=pedido)
            st.success(f"Pedido de '{musica}' enviado!")

# --- SEGUNDA TELA (Simulação de Anúncio) ---
st.markdown("---")
st.header("📺 Ecrã do DJ (Próximo Cantor)")

# Aqui vamos buscar os pedidos para numerá-los
pedidos_raw = requests.get(URL_FIREBASE_PEDIDOS).json() or {}
if pedidos_raw:
    lista_pedidos = list(pedidos_raw.values())
    for i, p in enumerate(lista_pedidos, 1):
        col1, col2 = st.columns([1, 4])
        with col1:
            st.metric("Pedido", f"#{i}")
        with col2:
            st.write(f"**Cantor:** {p['cantor']} | **Música:** {p['musica']}")
else:
    st.info("Nenhum pedido na fila.")
