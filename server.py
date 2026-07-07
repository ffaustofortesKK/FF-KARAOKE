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
    
    /* Botões: Cinza escuro, letra branca, hover amarelo */
    div.stButton > button {{ 
        background-color: #333333 !important; color: #FFFFFF !important; 
        font-weight: bold; border: 1px solid #555; transition: 0.3s;
    }}
    div.stButton > button:hover {{ background-color: #FFD700 !important; color: #000000 !important; }}
    
    /* Estilo Lista Á SEGUIR */
    .box-seguir {{ background: #111; padding: 20px; border: 2px solid #FFD700; border-radius: 10px; margin-top: 20px; }}
    .item-seguir {{ color: #FFD700; font-weight: bold; font-size: 18px; margin: 5px 0; }}
    </style>
""", unsafe_allow_html=True)

if 'registado' not in st.session_state: st.session_state.registado = False

# Layout Header
if st.session_state.registado:
    st.markdown(f'<div style="display:flex; justify-content:center;"><img src="{LINK_LOGO}" width="150"></div>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center; color:#FFD700; font-size:20px;">Bem-vindo, {st.session_state.nome}!</p>', unsafe_allow_html=True)
else:
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
        # --- Á SEGUIR (Lista de Pedidos) ---
        st.markdown('<div class="box-seguir"><h2>Á SEGUIR ➔</h2>', unsafe_allow_html=True)
        try:
            pedidos_resp = requests.get(URL_FIREBASE_PEDIDOS, timeout=5).json()
            if pedidos_resp:
                for i, (key, val) in enumerate(pedidos_resp.items(), 1):
                    st.markdown(f'<p class="item-seguir">{i}. {val.get("musica", "N/A")}</p>', unsafe_allow_html=True)
        except: st.write("Aguardando pedidos...")
        st.markdown('</div>', unsafe_allow_html=True)

        # BUSCA
        with st.form("form_busca", clear_on_submit=True):
            busca = st.text_input("Título / Cantor:")
            col_bts = st.columns([1, 1])
            with col_bts[0]:
                if st.form_submit_button("Pesquisar"):
                    try:
                        resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
                        dados = resp.json()
                        cat = list(dados.keys()) if isinstance(dados, dict) else dados
                        st.session_state.resultados = [m for m in cat if busca.lower() in m.lower()]
                    except: pass
            with col_bts[1]:
                if st.form_submit_button("Limpar Pesquisa"):
                    st.session_state.resultados = None
        
        if 'resultados' in st.session_state and st.session_state.resultados:
            escolha = st.selectbox("Selecione:", st.session_state.resultados, key="sel_musica")
            col_b1, col_b2 = st.columns([1, 1])
            with col_b1:
                if st.button("Confirmar Pedido"):
                    requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": escolha})
                    st.markdown('<div class="success-box">Pedido enviado com sucesso! 🎶</div>', unsafe_allow_html=True)
                    st.balloons()
                    st.session_state.resultados = None
                    st.rerun()
            with col_b2:
                if st.button("Limpar Pedido"):
                    st.session_state.resultados = None
                    st.rerun()
        
        # MANUAL
        with st.form("form_manual", clear_on_submit=True):
            manual = st.text_input("Não encontrou? Digite aqui:")
            if st.form_submit_button("Enviar Pedido Manual"):
                if manual:
                    requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": manual})
                    st.markdown('<div class="warning-box">Seu pedido foi enviado, mas nem todas as músicas existem na versão Karaoke. 🎶</div>', unsafe_allow_html=True)

    with col_cam:
        st.camera_input("Foto")
        if st.button("Sair"):
            st.session_state.registado = False
            st.rerun()
