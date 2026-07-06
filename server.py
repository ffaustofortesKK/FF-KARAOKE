import streamlit as st
import requests
import json

# --- CONFIGURAÇÕES ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"
LINK_LOGO = "https://cdn.phototourl.com/free/2026-07-03-793a0f18-6143-44c8-b56e-e44af828c30c.png"

st.set_page_config(page_title="FF KARAOKE CLOUD", layout="wide")

# --- CSS PERSONALIZADO ---
st.markdown(f"""
    <style>
    /* Fundo com Logotipo Fusco */
    .stApp {{ 
        background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%); 
        color: white; 
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: url('{LINK_LOGO}');
        background-position: center;
        background-repeat: no-repeat;
        background-size: contain;
        opacity: 0.1; /* Fusco */
        z-index: -1;
    }}
    
    /* Estilo do texto de confirmação */
    .confirma-social {{
        color: white !important;
        text-shadow: 2px 2px 4px #000000;
        text-decoration: underline;
        font-weight: bold;
    }}
    
    label {{ color: white !important; font-weight: bold; }}
    
    /* Inputs e Botões */
    div[data-baseweb="input"], div[data-baseweb="select"] {{ width: 50% !important; }}
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {{
        background-color: #FFFFFF !important; color: #000000 !important;
        border: 2px solid #D4AF37 !important; height: 40px !important;
    }}
    input {{ color: #000000 !important; font-weight: bold; }}
    div.stButton > button {{ background-color: #FFD700 !important; color: #000000 !important; font-weight: bold; width: 50%; }}
    .success-box {{ background-color: #008000; color: #FFFFFF; padding: 10px; border-radius: 5px; font-weight: bold; margin-top: 10px; width: 50%; }}
    .warning-box {{ background-color: #DAA520; color: #000000; padding: 10px; border-radius: 5px; font-weight: bold; margin-top: 10px; width: 50%; }}
    </style>
""", unsafe_allow_html=True)

if 'registado' not in st.session_state: st.session_state.registado = False

# Cabeçalho
st.markdown(f'<div style="display:flex; justify-content:center;"><img src="{LINK_LOGO}" width="250"></div>', unsafe_allow_html=True)

if not st.session_state.registado:
    st.subheader("📝 Registo Inicial")
    st.markdown("### 📱 Siga-nos para aceder ao Karaoke:")
    st.markdown("[📸 Seguir no Instagram @ff_karaoke](https://www.instagram.com/ff_karaoke)")
    st.markdown("[🎵 Seguir no TikTok @ff.karaoke](https://www.tiktok.com/@ff.karaoke)")
    
    st.write("---")
    nome = st.text_input("Nome:")
    
    # Texto customizado com sombra e sublinhado
    st.markdown('<p class="confirma-social">Confirmo que segui o Grupo FF no Instagram e no TikTok</p>', unsafe_allow_html=True)
    check_social = st.checkbox("Li e aceito")
    
    if st.button("Concluir Registo"):
        if nome and check_social:
            st.session_state.nome = nome
            st.session_state.registado = True
            st.rerun()
        else:
            st.error("Por favor, preencha o nome e confirme que seguiu as páginas!")

else:
    col_main, col_cam = st.columns([2, 1])
    
    with col_main:
        st.markdown(f'<p style="color:#FFD700; font-weight:bold; font-size:24px;">Bem-vindo, {st.session_state.nome}!</p>', unsafe_allow_html=True)
        
        # BUSCA
        busca = st.text_input("Título / Cantor:", key="input_busca")
        if st.button("Pesquisar"):
            try:
                resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
                dados = resp.json()
                cat = list(dados.keys()) if isinstance(dados, dict) else dados
                st.session_state.resultados = [m for m in cat if busca.lower() in m.lower()]
                st.rerun()
            except: pass

        if 'resultados' in st.session_state and st.session_state.resultados:
            escolha = st.selectbox("Selecione a música:", st.session_state.resultados, key="select_musica")
            if st.button("Confirmar Pedido"):
                requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": escolha})
                st.markdown('<div class="success-box">O seu pedido foi enviado com sucesso!</div>', unsafe_allow_html=True)
                st.balloons()
                st.session_state.resultados = None
                if 'select_musica' in st.session_state: del st.session_state['select_musica']
                st.session_state.input_busca = ""
                st.rerun()
        
        # PEDIDO MANUAL
        st.markdown("<br><label>Título/Cantor que não estão na lista:</label>", unsafe_allow_html=True)
        manual = st.text_input("Digite aqui manualmente:", key="input_manual")
        if st.button("Enviar Pedido Manual"):
            if manual:
                requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": manual})
                st.markdown('<div class="warning-box">Pedido enviado!</div>', unsafe_allow_html=True)
                st.session_state.input_manual = ""
                st.rerun()

    with col_cam:
        st.camera_input("Foto")
        if st.button("Sair"):
            st.session_state.registado = False
            st.rerun()
