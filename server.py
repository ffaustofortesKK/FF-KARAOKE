import streamlit as st
import requests
import base64
from io import BytesIO

# --- CONFIGURAÇÕES ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"
LINK_LOGO = "https://cdn.phototourl.com/free/2026-07-03-793a0f18-6143-44c8-b56e-e44af828c30c.png"
URL_SOM_PALMAS = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" # Substitua por um link de palmas real se desejar

st.set_page_config(page_title="FF KARAOKE CLOUD", layout="wide")

# CSS personalizado: Fundo com logo e estilo geral
st.markdown(f"""
<style>
.stApp {{ 
    background: linear-gradient(rgba(9, 10, 15, 0.8), rgba(9, 10, 15, 0.8)), url('{LINK_LOGO}');
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
    color: white; 
}}
</style>
""", unsafe_allow_html=True)

# Inicialização de estados
if 'registado' not in st.session_state: st.session_state.registado = False
if 'reset_key' not in st.session_state: st.session_state.reset_key = 0

def limpar_campos():
    st.session_state.reset_key += 1
    st.rerun()

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
    
    # BUSCA com Lupa
    busca = st.text_input("🔍 Pesquisar Música:", key=f"busca_{st.session_state.reset_key}")
    
    escolha = None
    if busca:
        try:
            resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
            dados = resp.json()
            cat = list(dados.keys()) if isinstance(dados, dict) else dados
            resultados = [m for m in cat if busca.lower() in m.lower()]
            escolha = st.selectbox("Selecione:", resultados, key=f"sel_{st.session_state.reset_key}")
        except: 
            st.error("Erro ao carregar catálogo.")

    # --- ENVIO ---
    if escolha:
        st.write(f"Música selecionada: **{escolha}**")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Confirmar Pedido"):
                payload = {
                    "cantor": st.session_state.nome, 
                    "musica": escolha,
                    "foto": None
                }
                requests.post(URL_FIREBASE_PEDIDOS, json=payload)
                
                # Efeitos
                st.audio(URL_SOM_PALMAS, autoplay=True)
                st.balloons()
                st.success("Pedido enviado com sucesso!")
                st.session_state.reset_key += 1
                st.rerun()
                
        with col2:
            if st.button("Limpar"):
                limpar_campos()

    st.markdown("---")
    if st.button("Sair"):
        st.session_state.registado = False
        st.rerun()
