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
    /* Logótipo Completo sem cortes */
    .logo-container { width: 100%; display: flex; justify-content: center; margin-bottom: 20px; }
    .logo-container img { width: 100% !important; max-width: 400px; height: auto !important; object-fit: contain; }
    
    /* Texto branco com sombra para leitura em fundo escuro */
    .stApp, label, p, div, .stCheckbox { color: white !important; text-shadow: 1px 1px 2px #000; }
    
    /* Inputs com texto branco e sombra */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background-color: #1a1a1a !important; 
        border: 2px solid #D4AF37 !important;
        color: white !important; 
        text-shadow: 1px 1px 2px #000;
        border-radius: 8px !important;
    }
    
    /* Texto Bem-vindo: Amarelo, Negrito e Maior */
    .welcome-text { color: #FFD700 !important; font-weight: bold; font-size: 28px !important; text-shadow: 2px 2px 4px #000; }
    
    /* Botões */
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
    check_social = st.checkbox("Confirmo que segui o Grupo FF nas Redes Sociais")
    
    if st.button("Concluir Registo"):
        if nome and check_social:
            st.session_state.nome = nome
            st.session_state.registado = True
            st.rerun()
        else:
            st.error("Preencha o nome e confirme as redes sociais!")
else:
    st.markdown(f'<p class="welcome-text">Bem-vindo, {st.session_state.nome}!</p>', unsafe_allow_html=True)
    
    # --- FASE 2: DASHBOARD ---
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("🎶 Pedido de Música")
        busca = st.text_input("Título / Cantor:")
        
        if st.button("Pesquisar na Nuvem"):
            try:
                resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
                dados = resp.json()
                cat = list(dados.keys()) if isinstance(dados, dict) else dados
                st.session_state.resultados_busca = [m for m in cat if busca.lower() in m.lower()]
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao ligar à nuvem: {e}")

        if st.session_state.resultados_busca:
            escolha = st.selectbox("Selecione a música:", st.session_state.resultados_busca)
            if st.button("Confirmar Pedido"):
                requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": escolha})
                st.success(f"Pedido de {escolha} enviado!")
                st.balloons() # Efeito de estrelas/fogo de artifício
                st.session_state.resultados_busca = None # Limpa a lista automaticamente
                st.rerun()
        elif st.session_state.resultados_busca == []:
            st.warning("Nenhuma música encontrada.")

        st.write("---")
        st.subheader("📝 Pedido Manual")
        manual = st.text_input("Não encontrou? Escreva manualmente:")
        if st.button("Enviar Pedido Manual"):
            if manual:
                requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": manual})
                st.warning("O seu pedido foi enviado!")

    with col2:
        st.camera_input("Foto")
        if st.button("Sair / Limpar"):
            st.session_state.registado = False
            st.session_state.resultados_busca = None
            st.rerun()
