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
    
    /* Botões Verde (Ação) */
    div.stButton > button.acao {{ background-color: #28a745 !important; color: white !important; font-weight: bold; }}
    /* Botões Vermelho (Limpar) */
    div.stButton > button.limpar {{ background-color: #dc3545 !important; color: white !important; font-weight: bold; }}
    </style>
""", unsafe_allow_html=True)

# Helper para aplicar estilos aos botões
def btn_verde(label): return st.button(label, key=f"btn_v_{label}", help="Ação", use_container_width=False, type="primary")
def btn_vermelho(label): return st.button(label, key=f"btn_r_{label}", help="Limpar")

if 'registado' not in st.session_state: st.session_state.registado = False
if 'resultados' not in st.session_state: st.session_state.resultados = None

st.markdown(f'<div style="display:flex; justify-content:center;"><img src="{LINK_LOGO}" width="250"></div>', unsafe_allow_html=True)

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
        st.markdown(f'<p style="color:#FFD700; font-weight:bold; font-size:24px;">Bem-vindo, {st.session_state.nome}!</p>', unsafe_allow_html=True)
        
        # BUSCA
        busca = st.text_input("Título / Cantor:")
        c1, c2 = st.columns([1, 4])
        with c1: 
            if st.button("🔍 Pesquisar", key="pesq"):
                try:
                    resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
                    dados = resp.json()
                    cat = list(dados.keys()) if isinstance(dados, dict) else dados
                    st.session_state.resultados = [m for m in cat if busca.lower() in m.lower()]
                    st.rerun()
                except: pass
        with c2:
            if st.button("❌ Limpar Pesquisa"):
                st.session_state.resultados = None
                st.rerun()

        if st.session_state.resultados:
            escolha = st.selectbox("Selecione a música:", st.session_state.resultados)
            c3, c4 = st.columns([1, 4])
            with c3:
                if st.button("✅ Confirmar Pedido"):
                    requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": escolha})
                    for _ in range(5): st.toast("🎵") # Efeito de nota subindo
                    st.session_state.resultados = None
                    st.rerun()
            with c4:
                if st.button("❌ Limpar Pedido"):
                    st.session_state.resultados = None
                    st.rerun()

        # PEDIDO MANUAL
        st.markdown("<br><label>Título/Cantor não listado:</label>", unsafe_allow_html=True)
        manual = st.text_input("Digite manualmente:")
        if st.button("Enviar Pedido Manual"):
            if manual:
                requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": manual})
                st.warning("Seu pedido foi enviado, mas nem todas as músicas existem na versão Karaoke.")
                st.rerun()

    with col_cam:
        st.camera_input("Foto")
        if st.button("Sair"):
            st.session_state.registado = False
            st.rerun()
