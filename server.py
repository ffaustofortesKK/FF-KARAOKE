import streamlit as st
import requests
import time # Importado para pausar antes do rerun

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

    # 1. BUSCA PRINCIPAL
    busca = st.text_input("🔍 Pesquisar Música no catálogo:")

    escolha = None
    if busca:
        try:
            resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
            dados = resp.json()
            
            # --- FUNÇÃO DE PESQUISA CORRIGIDA ---
            # Acede à chave "catalogo" e extrai apenas os nomes das músicas (valores)
            if isinstance(dados, dict) and "catalogo" in dados:
                cat = list(dados["catalogo"].values())
            else:
                cat = []
            
            resultados = [m for m in cat if busca.lower() in m.lower()]
            # ------------------------------------
            
            escolha = st.selectbox("Selecione:", resultados)
        except: 
            escolha = None
            st.error("Erro ao carregar catálogo.")

    # --- ENVIO CATALOGO ---
    if escolha:
        st.write(f"Música selecionada: **{escolha}**")
        if st.button("Confirmar Pedido"):
            requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": escolha})

            # EFEITOS E MENSAGENS
            st.balloons()
            st.success("O seu pedido foi enviado com sucesso!")
            st.audio(URL_SOM_PALMAS, autoplay=True)

            time.sleep(2) # Pausa para o utilizador ler a mensagem
            st.rerun()

    st.divider()

    # 2. CAMPO PEDIDO MANUAL
    st.subheader("Manual")
    pedido_manual = st.text_input("Não achou? Digite o nome da música:")

    if st.button("Confirmar Pedido Manual"):
        if pedido_manual:
            payload = {
                "cantor": st.session_state.nome, 
                "musica": pedido_manual,
                "status": "manual"
            }
            requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": pedido_manual, "status": "manual"})

            # EFEITOS E MENSAGENS
            st.balloons()
            st.success("O seu pedido foi enviado com sucesso!")
            st.warning("Nota: O seu pedido foi enviado, mas nem todas as músicas existem em Karaoke.")

            time.sleep(3) # Pausa maior devido ao aviso
            st.rerun()
        else:
            st.error("Por favor, digite o nome da música.")

    if st.button("Sair"):
        st.session_state.registado = False
        st.rerun()
