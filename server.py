import streamlit as st
import requests
import base64

# --- CONFIGURAÇÕES ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"
LINK_LOGO = "https://cdn.phototourl.com/free/2026-07-03-793a0f18-6143-44c8-b56e-e44af828c30c.png"
URL_PALMAS = "https://actions.google.com/sounds/v1/crowd/clapping.ogg" # Som de palmas

st.set_page_config(page_title="FF KARAOKE CLOUD", layout="wide")

# CSS: Fundo, Lupa na pesquisa e ajuste de visual
st.markdown(f"""
<style>
    .stApp {{ 
        background: url('{LINK_LOGO}') no-repeat center center fixed; 
        background-size: cover;
        background-color: #090A0F;
        color: white; 
    }}
    /* Adiciona ícone de lupa no campo de texto */
    div[data-testid="stTextInput"] > div > div > input {{
        padding-left: 30px !important;
    }}
    div[data-testid="stTextInput"]::before {{
        content: "🔍";
        position: absolute;
        left: 10px;
        top: 35px;
        z-index: 10;
        pointer-events: none;
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
    # A estrutura foi simplificada para remover a câmera e focar no pedido
    st.title(f"Bem-vindo, {st.session_state.nome}!")
    
    # BUSCA (com estilo de lupa via CSS acima)
    busca = st.text_input("Pesquisar Música:")
    
    escolha = None
    if busca:
        try:
            resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
            dados = resp.json()
            cat = list(dados.keys()) if isinstance(dados, dict) else dados
            resultados = [m for m in cat if busca.lower() in m.lower()]
            if resultados:
                escolha = st.selectbox("Selecione:", resultados)
        except: 
            st.error("Erro ao carregar catálogo.")

    # --- ENVIO DO PEDIDO ---
    if escolha:
        st.write(f"Música selecionada: **{escolha}**")
        
        if st.button("Confirmar Pedido"):
            payload = {
                "cantor": st.session_state.nome, 
                "musica": escolha,
                "foto": None # Câmera removida conforme solicitado
            }
            requests.post(URL_FIREBASE_PEDIDOS, json=payload)
            
            # Efeito de sucesso e som de palmas
            st.success("Pedido enviado com sucesso!")
            st.balloons()
            
            # Script para reproduzir o som de palmas
            st.markdown(f"""
                <audio autoplay>
                    <source src="{URL_PALMAS}" type="audio/ogg">
                </audio>
            """, unsafe_allow_html=True)

    if st.button("Sair"):
        st.session_state.registado = False
        st.rerun()
