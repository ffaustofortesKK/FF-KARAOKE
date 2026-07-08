import streamlit as st
import requests
import base64

# --- CONFIGURAÇÕES ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"
LINK_LOGO = "https://cdn.phototourl.com/free/2026-07-03-793a0f18-6143-44c8-b56e-e44af828c30c.png"
LINK_PALMAS = "https://www.myinstants.com/media/sounds/applause.mp3" # Som de palmas

st.set_page_config(page_title="FF KARAOKE CLOUD", layout="wide")

# CSS: Fundo fixo com logo e ajuste de estilo
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url('{LINK_LOGO}');
        background-size: 200px;
        background-repeat: no-repeat;
        background-position: bottom right;
        background-color: #090A0F;
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
    
    # BUSCA COM LUPA
    busca = st.text_input("🔍 Pesquisar Música:")
    
    if busca:
        try:
            resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
            dados = resp.json()
            cat = list(dados.keys()) if isinstance(dados, dict) else dados
            resultados = [m for m in cat if busca.lower() in m.lower()]
            escolha = st.selectbox("Selecione:", resultados)
        except: 
            escolha = None
            st.error("Erro ao conectar ao catálogo.")
    else: 
        escolha = None

    # --- ENVIO DO PEDIDO ---
    if escolha:
        st.write(f"Música selecionada: **{escolha}**")
        
        if st.button("Confirmar Pedido"):
            payload = {
                "cantor": st.session_state.nome, 
                "musica": escolha,
                "foto": None # Foto removida conforme solicitado
            }
            requests.post(URL_FIREBASE_PEDIDOS, json=payload)
            st.success("Pedido enviado com sucesso!")
            
            # Efeito de som de palmas (HTML5 invisível)
            st.markdown(f"""
                <audio autoplay>
                  <source src="{LINK_PALMAS}" type="audio/mp3">
                </audio>
            """, unsafe_allow_html=True)
            
            st.balloons()

    # BOTOES EXISTENTES
    if st.button("Sair"):
        st.session_state.registado = False
        st.rerun()
