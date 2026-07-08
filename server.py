import streamlit as st
import requests
import base64

# --- CONFIGURAÇÕES ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"
LINK_LOGO = "https://cdn.phototourl.com/free/2026-07-03-793a0f18-6143-44c8-b56e-e44af828c30c.png"
LINK_SOM_PALMAS = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" # Substitua por um link direto de palmas se preferir

st.set_page_config(page_title="FF KARAOKE CLOUD", layout="wide")

# CSS personalizado: Fundo com Logo e ajuste de transparência
st.markdown(f"""
    <style>
    .stApp {{ 
        background-image: url('{LINK_LOGO}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .stApp > div {{ background-color: rgba(9, 10, 15, 0.85); padding: 20px; border-radius: 10px; }}
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
    # --- LAYOUT SIMPLIFICADO ---
    st.title(f"Bem-vindo, {st.session_state.nome}!")
    
    # BUSCA COM LUPA
    busca = st.text_input("🔍 Pesquisar Música:")
    
    escolha = None
    if busca:
        try:
            resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
            dados = resp.json()
            cat = list(dados.keys()) if isinstance(dados, dict) else dados
            resultados = [m for m in cat if busca.lower() in m.lower()]
            escolha = st.selectbox("Selecione:", resultados)
        except: 
            st.error("Erro ao carregar catálogo.")

    # --- ENVIO ---
    if escolha:
        st.write(f"Música selecionada: **{escolha}**")
        
        if st.button("Confirmar Pedido"):
            payload = {
                "cantor": st.session_state.nome, 
                "musica": escolha,
                "foto": None # Foto removida conforme solicitado
            }
            requests.post(URL_FIREBASE_PEDIDOS, json=payload)
            
            # Feedback Visual e Sonoro
            st.success("Pedido enviado com sucesso!")
            st.balloons()
            st.audio(LINK_SOM_PALMAS, autoplay=True)

    if st.button("Sair"):
        st.session_state.registado = False
        st.rerun()
