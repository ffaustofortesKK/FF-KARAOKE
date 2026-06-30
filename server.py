import streamlit as st
import requests
import json

# --- CONFIGURAÇÕES ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"

st.set_page_config(page_title="FF KARAOKE CLOUD", layout="wide")

# --- CSS PERSONALIZADO ---
st.markdown("""
    <style>
    /* Logótipo Completo e sem cortes */
    .logo-container { width: 100%; display: flex; justify-content: center; }
    .logo-container img { width: 100% !important; max-width: 400px; height: auto !important; }
    
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
    st.success(f"Bem-vindo, {st.session_state.nome}!")
    
    # --- FASE 2: DASHBOARD ---
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("🎶 Pedido de Música")
        busca = st.text_input("Título / Cantor:")
        
        # Botão Pesquisar que força o recarregamento
        if st.button("Pesquisar na Nuvem"):
            try:
                resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
                # Verifica se o Firebase retorna um dicionário ou lista
                dados = resp.json()
                cat = list(dados.keys()) if isinstance(dados, dict) else dados
                st.session_state.resultados_busca = [m for m in cat if busca.lower() in m.lower()]
                st.rerun() # OBRIGATÓRIO: força o app a mostrar o que encontrou
            except Exception as e:
                st.error(f"Erro ao ligar à nuvem: {e}")

        # Se encontrou algo, mostra a lista
        if st.session_state.resultados_busca:
            escolha = st.selectbox("Selecione a música:", st.session_state.resultados_busca)
            if st.button("Confirmar Pedido"):
                requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": escolha})
                st.success(f"Pedido de {escolha} enviado!")
                st.session_state.resultados_busca = None
        elif st.session_state.resultados_busca == []:
            st.warning("Nenhuma música encontrada.")

        st.write("---")
        st.subheader("📝 Pedido Manual")
        manual = st.text_input("Não encontrou? Escreva manualmente:")
        if st.button("Enviar Pedido Manual"):
            if manual:
                requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": manual})
                st.warning("O seu pedido foi enviado, mas nem todas as músicas estão disponíveis em Karaoke.")

    with col2:
        st.camera_input("Foto")
        if st.button("Sair / Limpar"):
            st.session_state.registado = False
            st.session_state.resultados_busca = None
            st.rerun()
