import streamlit as st
import requests

# --- CONFIGURAÇÕES ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"
LINK_LOGO = "https://cdn.phototourl.com/free/2026-07-03-793a0f18-6143-44c8-b56e-e44af828c30c.png"

st.set_page_config(page_title="FF KARAOKE CLOUD", layout="wide")

# --- CSS PERSONALIZADO ---
st.markdown(f"""
    <style>
    .stApp {{ background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%); color: white; }}
    .stApp::before {{
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background-image: url('{LINK_LOGO}'); background-position: center;
        background-repeat: no-repeat; background-size: contain; opacity: 0.1; z-index: -1;
    }}
    .confirma-social {{ color: white !important; text-shadow: 2px 2px 4px #000000; text-decoration: underline; font-weight: bold; }}
    label {{ color: white !important; font-weight: bold; }}
    div[data-baseweb="input"], div[data-baseweb="select"] {{ width: 40% !important; }}
    /* Botoes Cinza Escuro */
    div.stButton > button {{ background-color: #333333 !important; color: #FFFFFF !important; font-weight: bold; border: 1px solid #555; }}
    .success-box {{ background-color: #008000; color: #FFFFFF; padding: 10px; border-radius: 5px; font-weight: bold; width: 40%; }}
    .warning-box {{ background-color: #DAA520; color: #000000; padding: 10px; border-radius: 5px; font-weight: bold; width: 40%; }}
    </style>
""", unsafe_allow_html=True)

if 'registado' not in st.session_state: st.session_state.registado = False

st.markdown(f'<div style="display:flex; justify-content:center;"><img src="{LINK_LOGO}" width="200"></div>', unsafe_allow_html=True)

if not st.session_state.registado:
    st.subheader("📝 Registo Inicial")
    st.markdown("[📸 Instagram: @ff_karaoke](https://www.instagram.com/ff_karaoke)")
    st.markdown("[🎵 TikTok: @ff.karaoke](https://www.tiktok.com/@ff.karaoke)")
    nome = st.text_input("Nome:")
    st.markdown('<p class="confirma-social">Confirmo que segui o Grupo FF no Instagram e no TikTok</p>', unsafe_allow_html=True)
    check_social = st.checkbox("Li e aceito")
    if st.button("Concluir Registo"):
        if nome and check_social:
            st.session_state.nome = nome
            st.session_state.registado = True
            st.rerun()
else:
    col_main, col_cam = st.columns([2, 1])
    
    with col_main:
        st.markdown(f'<p style="color:#FFD700; font-weight:bold; font-size:20px;">Bem-vindo, {st.session_state.nome}!</p>', unsafe_allow_html=True)
        
        # BUSCA COM FORMULÁRIO (Limpa sozinho)
        with st.form("form_busca", clear_on_submit=True):
            busca = st.text_input("Título / Cantor:")
            col_b1, col_b2 = st.columns([1, 4])
            with col_b1:
                btn_pesquisar = st.form_submit_button("Pesquisar")
            with col_b2:
                btn_limpar = st.form_submit_button("Limpar Pesquisa")
            
            if btn_pesquisar and busca:
                try:
                    resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
                    dados = resp.json()
                    cat = list(dados.keys()) if isinstance(dados, dict) else dados
                    st.session_state.resultados = [m for m in cat if busca.lower() in m.lower()]
                except: pass
            if btn_limpar:
                st.session_state.resultados = None

        if 'resultados' in st.session_state and st.session_state.resultados:
            escolha = st.selectbox("Selecione a música:", st.session_state.resultados)
            if st.button("Confirmar Pedido"):
                requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": escolha})
                st.markdown('<div class="success-box">Pedido enviado! 🎶🎵🎶🎵</div>', unsafe_allow_html=True)
                st.balloons()
                st.session_state.resultados = None
                st.rerun()
        
        # MANUAL COM FORMULÁRIO (Limpa sozinho)
        with st.form("form_manual", clear_on_submit=True):
            st.markdown("<label>Título/Cantor não listado:</label>", unsafe_allow_html=True)
            manual = st.text_input("Manual:")
            if st.form_submit_button("Enviar Pedido Manual"):
                if manual:
                    requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": manual})
                    st.markdown('<div class="warning-box">Seu pedido foi enviado, mas nem todas as músicas existem na versão Karaoke.</div>', unsafe_allow_html=True)

    with col_cam:
        st.camera_input("Foto")
        if st.button("Sair"):
            st.session_state.registado = False
            st.rerun()
