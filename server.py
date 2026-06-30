import streamlit as st
import requests
import json

# --- CONFIGURAÇÕES ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"

st.set_page_config(page_title="FF KARAOKE CLOUD", layout="wide")

# --- CSS E LÓGICA DE ESTADO ---
st.markdown("""
    <style>
    .logo-container { display: flex; justify-content: center; }
    .logo-container img { width: 30% !important; }
    .stApp { background-color: #000000; color: #D4AF37; }
    label { color: white !important; font-weight: bold; }
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background-color: #1a1a1a !important; border: 2px solid #D4AF37 !important;
        color: #D4AF37 !important; border-radius: 8px !important;
    }
    div.stButton > button { background-color: #D4AF37 !important; color: #000 !important; font-weight: bold; width: 100%; }
    </style>
""", unsafe_allow_html=True)

if 'registado' not in st.session_state: st.session_state.registado = False
if 'resultados_busca' not in st.session_state: st.session_state.resultados_busca = None

# --- CABEÇALHO ---
st.markdown('<div class="logo-container"><img src="https://i.ibb.co/HfKTnDDQ/logoweb.png"></div>', unsafe_allow_html=True)

# --- FASE 1: REGISTO ---
if not st.session_state.registado:
    st.subheader("📝 Registo Inicial")
    nome = st.text_input("Nome:")
    st.markdown("[👉 Seguir no TikTok](https://www.tiktok.com/@ff_karaoke) | [👉 Seguir no Instagram](https://www.instagram.com/ff.karaoke/)")
    check_social = st.checkbox("Confirmo que segui o Grupo FF nas redes sociais.")
    
    if st.button("Concluir Registo"):
        if nome and check_social:
            st.session_state.nome = nome
            st.session_state.registado = True
            st.rerun()
        else:
            st.error("Preencha o nome e confirme as redes sociais!")
else:
    # --- FASE 2: DASHBOARD ---
    st.success(f"Bem-vindo, {st.session_state.nome}!")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("🎶 Pedido de Música")
        c1, c2 = st.columns([3, 1])
        with c1:
            busca = st.text_input("Título / Cantor:")
        with c2:
            st.write("###") 
            if st.button("Pesquisar"):
                # Carregar catálogo e filtrar
                try:
                    resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
                    cat = list(resp.json().keys()) if resp.status_code == 200 else []
                    st.session_state.resultados_busca = [m for m in cat if busca.lower() in m.lower()]
                except:
                    st.session_state.resultados_busca = []

        # Mostrar resultados se existirem na memória da sessão
        if st.session_state.resultados_busca:
            escolha = st.selectbox("Selecione a música:", st.session_state.resultados_busca)
            if st.button("Confirmar Pedido da Nuvem"):
                requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": escolha})
                st.success(f"Pedido de {escolha} enviado!")
                st.session_state.resultados_busca = None # Limpa após enviar
        elif st.session_state.resultados_busca == []:
            st.warning("Nenhuma música encontrada.")

        st.write("---")
        st.subheader("📝 Pedido Manual")
        manual = st.text_input("Escreva manualmente se não encontrou:")
        if st.button("Enviar Pedido Manual"):
            if manual:
                requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": manual})
                st.warning("O seu pedido foi enviado, mas nem todas as músicas estão disponíveis em Karaoke.")

    with col2:
        st.camera_input("Foto")
        if st.button("Sair / Limpar"):
            st.session_state.registado = False
            st.rerun()
