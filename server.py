import streamlit as st
import requests
import time 

# --- CONFIGURAÇÕES ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"
LINK_LOGO = "https://cdn.phototourl.com/free/2026-07-03-793a0f18-6143-44c8-b56e-e44af828c30c.png"
URL_SOM_PALMAS = "https://www.soundjay.com/misc/sounds/applause-2.mp3"

st.set_page_config(page_title="FF KARAOKE CLOUD", layout="wide")

# CSS personalizado
st.markdown(f"""
    <style>
    .stApp {{ 
        background: linear-gradient(rgba(9, 10, 15, 0.85), rgba(9, 10, 15, 0.85)), url('{LINK_LOGO}');
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        color: white; 
    }}
    </style>
""", unsafe_allow_html=True)

# Função para carregar o catálogo de forma estável
@st.cache_data(ttl=60)
def carregar_catalogo():
    try:
        resp = requests.get(URL_FIREBASE_CATALOGO, timeout=10)
        dados = resp.json()
        if isinstance(dados, dict):
            # Se encontrar a chave "catalogo", extrai os valores
            if "catalogo" in dados:
                return list(dados["catalogo"].values())
            # Se não, tenta extrair os valores diretamente
            return list(dados.values())
        return []
    except:
        return []

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
    st.title(f"Bem-vindo, {st.session_state.nome}!")
    
    # Carregar catálogo uma vez
    catalogo_completo = carregar_catalogo()
    
    # 1. BUSCA PRINCIPAL
    busca = st.text_input("🔍 Pesquisar Música no catálogo:")
    
    escolha = None
    if busca and catalogo_completo:
        resultados = [m for m in catalogo_completo if busca.lower() in str(m).lower()]
        if resultados:
            escolha = st.selectbox("Selecione:", resultados)
        else:
            st.write("Nenhuma música encontrada com esse termo.")

    # --- ENVIO CATALOGO ---
    if escolha:
        st.write(f"Música selecionada: **{escolha}**")
        if st.button("Confirmar Pedido"):
            requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": escolha})
            st.balloons()
            st.success("O seu pedido foi enviado com sucesso!")
            st.audio(URL_SOM_PALMAS, autoplay=True)
            time.sleep(2) 
            st.rerun()

    st.divider()

    # 2. CAMPO PEDIDO MANUAL
    st.subheader("Manual")
    pedido_manual = st.text_input("Não achou? Digite o nome da música:")
    
    if st.button("Confirmar Pedido Manual"):
        if pedido_manual:
            payload = {"cantor": st.session_state.nome, "musica": pedido_manual, "status": "manual"}
            requests.post(URL_FIREBASE_PEDIDOS, json=payload)
            st.balloons()
            st.success("O seu pedido foi enviado com sucesso!")
            st.warning("Nota: O seu pedido foi enviado, mas nem todas as músicas existem em Karaoke.")
            time.sleep(3) 
            st.rerun()
        else:
            st.error("Por favor, digite o nome da música.")

    if st.button("Sair"):
        st.session_state.registado = False
        st.rerun()
