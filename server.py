import streamlit as st
import requests
import time 

# --- CONFIGURAÇÕES ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"
LINK_LOGO = "https://cdn.phototourl.com/free/2026-07-03-793a0f18-6143-44c8-b56e-e44af828c30c.png"
URL_SOM_PALMAS = "https://www.soundjay.com/misc/sounds/applause-2.mp3"

st.set_page_config(page_title="FF KARAOKE CLOUD", layout="wide")

@st.cache_data(ttl=300)
def obter_catalogo():
    try:
        resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
        dados = resp.json()
        if isinstance(dados, list):
            return dados
        if isinstance(dados, dict):
            return list(dados.values())
        return []
    except:
        return []

def verificar_pedido_ativo(nome_cantor):
    """Verifica se o cantor já possui um pedido pendente na base de dados."""
    try:
        resp = requests.get(URL_FIREBASE_PEDIDOS, timeout=5)
        dados = resp.json()
        if not dados:
            return False
        
        # O Firebase retorna um dicionário com IDs únicos como chaves
        if isinstance(dados, dict):
            for pedido_id, info in dados.items():
                if isinstance(info, dict) and info.get("cantor", "").strip().lower() == nome_cantor.strip().lower():
                    # Se o pedido ainda está ativo (podes ajustar a regra de status se necessário)
                    return True
        elif isinstance(dados, list):
            for info in dados:
                if isinstance(info, dict) and info.get("cantor", "").strip().lower() == nome_cantor.strip().lower():
                    return True
        return False
    except:
        return False

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

    # Verificar se o utilizador já tem um pedido na fila
    tem_pedido_ativo = verificar_pedido_ativo(st.session_state.nome)

    if tem_pedido_ativo:
        st.warning("⚠️ Você já tem uma música na fila! Só poderá enviar um novo pedido assim que a sua música atual for finalizada.")
        
        # Botão para atualizar a página e verificar se já foi atendido
        if st.button("🔄 Atualizar Status"):
            st.rerun()
    else:
        # --- 1. PESQUISA NO CATÁLOGO ---
        busca = st.text_input("🔍 Pesquisar Música no catálogo:")

        escolha = None
        if busca:
            cat = obter_catalogo()
            resultados = [m for m in cat if busca.lower() in str(m).lower()]
            
            if resultados:
                escolha = st.selectbox("Selecione:", resultados)

        # --- ENVIO CATALOGO ---
        if escolha:
            st.write(f"Música selecionada: **{escolha}**")
            if st.button("Confirmar Pedido"):
                requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": str(escolha).strip()})
                st.balloons()
                st.success("O seu pedido foi enviado com sucesso!")
                st.audio(URL_SOM_PALMAS, autoplay=True)
                time.sleep(2)
                st.rerun()

        st.divider()

        # --- 2. CAMPO PEDIDO MANUAL ---
        st.subheader("Manual")
        pedido_manual = st.text_input("Não achou? Digite o nome da música:")

        if st.button("Confirmar Pedido Manual"):
            if pedido_manual and pedido_manual.strip():
                payload = {
                    "cantor": st.session_state.nome, 
                    "musica": pedido_manual.strip(), 
                    "status": "manual"
                }
                requests.post(URL_FIREBASE_PEDIDOS, json=payload)
                st.balloons()
                st.success("O seu pedido foi enviado com sucesso!")
                st.warning("Nota: O seu pedido foi enviado, mas nem todas as músicas existem em Karaoke.")
                time.sleep(3)
                st.rerun()
            else:
                st.error("Por favor, digite o nome da música.")

    st.divider()
    if st.button("Sair"):
        st.session_state.registado = False
        st.rerun()
