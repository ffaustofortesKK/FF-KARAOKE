import streamlit as st
import requests

# --- CONFIGURAÇÕES ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"
LINK_LOGO = "https://cdn.phototourl.com/free/2026-07-03-793a0f18-6143-44c8-b56e-e44af828c30c.png"

# Links das suas imagens de fundo (substitua pelos links reais das imagens enviadas)
IMG_REGISTO = "URL_DA_SUA_IMAGEM_REGISTO" 
IMG_PEDIDO = "URL_DA_SUA_IMAGEM_MICROFONE"

st.set_page_config(page_title="FF KARAOKE CLOUD", layout="wide")

# --- CSS PERSONALIZADO ---
st.markdown(f"""
    <style>
    .stApp {{ color: white; }}
    
    /* Fundo Registo */
    .fundo-registro {{
        background-image: url('{IMG_REGISTO}');
        background-size: cover; background-position: center; background-attachment: fixed;
    }}
    
    /* Fundo Pedido */
    .fundo-pedido {{
        background-image: url('{IMG_PEDIDO}');
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    .confirma-social {{ color: white !important; text-shadow: 2px 2px 4px #000000; text-decoration: underline; font-weight: bold; }}
    label {{ color: white !important; font-weight: bold; }}
    div[data-baseweb="input"], div[data-baseweb="select"] {{ width: 40% !important; }}
    
    div.stButton > button {{ 
        background-color: #333333 !important; color: #FFFFFF !important; 
        font-weight: bold; border: 1px solid #555; transition: 0.3s;
    }}
    div.stButton > button:hover {{ background-color: #FFD700 !important; color: #000000 !important; }}
    
    .success-box {{ background-color: #008000; color: #FFFFFF; padding: 10px; border-radius: 5px; font-weight: bold; width: 40%; }}
    .warning-box {{ background-color: #DAA520; color: #000000; padding: 10px; border-radius: 5px; font-weight: bold; width: 40%; }}
    </style>
""", unsafe_allow_html=True)

if 'registado' not in st.session_state: st.session_state.registado = False

# Aplicação dinâmica do fundo
if not st.session_state.registado:
    st.markdown('<script>document.querySelector("div.stApp").className += " fundo-registro";</script>', unsafe_allow_html=True)
else:
    st.markdown('<script>document.querySelector("div.stApp").className += " fundo-pedido";</script>', unsafe_allow_html=True)

# Lógica do Conteúdo
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
        
        # BUSCA
        with st.form("form_busca", clear_on_submit=True):
            busca = st.text_input("Título / Cantor:")
            c1, c2 = st.columns(2)
            if c1.form_submit_button("Pesquisar"):
                # Lógica de busca...
                pass
            if c2.form_submit_button("Limpar"):
                st.session_state.resultados = None
        
        # ... (Restante do seu código de pedidos)

    with col_cam:
        st.camera_input("Foto")
        if st.button("Sair"):
            st.session_state.registado = False
            st.rerun()
