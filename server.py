import streamlit as st
import requests
import json

# --- CONFIGURAÇÕES ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"

st.set_page_config(page_title="FF KARAOKE CLOUD", layout="wide")

# --- LÓGICA DE SESSÃO (Estado) ---
if 'registado' not in st.session_state: st.session_state.registado = False
if 'nome' not in st.session_state: st.session_state.nome = ""

# --- CSS (Redução do Logo e Estilo) ---
st.markdown("""
    <style>
    .logo-container { display: flex; justify-content: center; }
    .logo-container img { width: 30% !important; } /* Redução para 30% (aprox. 70% menor) */
    .stApp { background-color: #000000; color: #D4AF37; }
    label { color: white !important; font-weight: bold; }
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background-color: #1a1a1a !important; border: 2px solid #D4AF37 !important;
        color: #D4AF37 !important; border-radius: 8px !important;
    }
    div.stButton > button { background-color: #D4AF37 !important; color: #000 !important; font-weight: bold; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# --- CABEÇALHO COM LOGO REDUZIDO ---
st.markdown('<div class="logo-container"><img src="https://i.ibb.co/HfKTnDDQ/logoweb.png"></div>', unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #D4AF37;'>INSTAGRAM: ff_karaoke | TIK TOK: ff.karaoke</h4>", unsafe_allow_html=True)

# --- FASE 1: REGISTO (Só aparece se não estiver registado) ---
if not st.session_state.registado:
    st.subheader("📝 Registo Inicial")
    with st.form("registo"):
        nome = st.text_input("Nome:")
        pref = st.radio("Preferência musical:", ["Internacional", "Nacional"])
        agenda = st.radio("Quer acompanhar agenda de Karaoke do Grupo FF?", ["Sim", "Não"])
        if st.form_submit_button("Concluir Registo"):
            if nome:
                st.session_state.nome = nome
                st.session_state.registado = True
                st.rerun()
            else: st.error("Insira o seu nome!")
else:
    # --- FASE 2: DASHBOARD (Já está registado) ---
    st.success(f"Bem-vindo, {st.session_state.nome}!")
    if st.button("Limpar Registo"):
        st.session_state.registado = False
        st.rerun()

    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🔍 Pesquisa de Música")
        busca = st.text_input("Digite o título ou cantor:")
        
        # Carregar catálogo
        @st.cache_data(ttl=300)
        def carregar():
            try:
                resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
                return list(resp.json().keys()) if resp.status_code == 200 else []
            except: return []
        
        catalogo = carregar()
        
        if busca:
            resultados = [m for m in catalogo if busca.lower() in m.lower()]
            if resultados:
                escolha = st.selectbox("Músicas encontradas:", resultados)
                if st.button("Enviar Música Encontrada"):
                    dados = {"cantor": st.session_state.nome, "musica": escolha}
                    requests.post(URL_FIREBASE_PEDIDOS, json=dados)
                    st.success("Pedido enviado!")
        
        st.write("---")
        st.subheader("📝 Pedido ao Grupo FF")
        manual = st.text_input("Título / Cantor (Pedido Manual):")
        if st.button("Enviar Pedido Manual"):
            if manual:
                dados = {"cantor": st.session_state.nome, "musica": manual}
                requests.post(URL_FIREBASE_PEDIDOS, json=dados)
                st.warning("O seu pedido foi enviado, mas nem todas as musicas estão disponíveis em Karaoke.")

    with col2:
        st.subheader("📸 Foto")
        st.camera_input("")
