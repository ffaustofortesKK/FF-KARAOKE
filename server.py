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
    .logo-container { display: flex; justify-content: center; }
    .logo-container img { width: 30% !important; }
    .stApp { background-color: #000000; color: #D4AF37; }
    label { color: white !important; font-weight: bold; }
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background-color: #1a1a1a !important; border: 2px solid #D4AF37 !important;
        color: #D4AF37 !important; border-radius: 8px !important;
    }
    div.stButton > button { background-color: #D4AF37 !important; color: #000 !important; font-weight: bold; width: 100%; }
    .social-links { text-align: center; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- CABEÇALHO ---
st.markdown('<div class="logo-container"><img src="https://i.ibb.co/HfKTnDDQ/logoweb.png"></div>', unsafe_allow_html=True)

# --- LÓGICA DE REGISTO ---
if 'registado' not in st.session_state: st.session_state.registado = False

if not st.session_state.registado:
    st.subheader("📝 Registo Inicial")
    nome = st.text_input("Nome:")
    pref = st.radio("Preferência musical:", ["Internacional", "Nacional"])
    
    st.write("### 📲 Siga-nos para continuar:")
    st.markdown("""
        [👉 Seguir no TikTok](https://www.tiktok.com/@ff_karaoke)  
        [👉 Seguir no Instagram](https://www.instagram.com/ff.karaoke/)
    """)
    
    check_social = st.checkbox("Confirmo que segui o Grupo FF nas redes sociais acima.")
    
    if st.button("Concluir Registo"):
        if nome and check_social:
            st.session_state.nome = nome
            st.session_state.registado = True
            st.rerun()
        else:
            st.error("Por favor, preencha o nome e confirme que seguiu as nossas redes!")

else:
    # --- DASHBOARD ---
    st.success(f"Bem-vindo, {st.session_state.nome}!")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("🎶 Pedido de Música")
        # Campo Título/Cantor com botão de pesquisa ao lado
        c1, c2 = st.columns([3, 1])
        with c1:
            busca = st.text_input("Título / Cantor:")
        with c2:
            st.write("###") # Espaçamento
            pesquisar = st.button("Pesquisar")
        
        if pesquisar and busca:
            @st.cache_data(ttl=300)
            def carregar():
                try:
                    resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
                    return list(resp.json().keys()) if resp.status_code == 200 else []
                except: return []
            
            res = [m for m in carregar() if busca.lower() in m.lower()]
            if res:
                escolha = st.selectbox("Selecione a opção:", res)
                if st.button("Confirmar Pedido"):
                    requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": escolha})
                    st.success("Pedido enviado!")
            else:
                st.warning("Não encontrada no catálogo. Use o pedido manual abaixo.")

        st.write("---")
        st.subheader("📝 Pedido Manual")
        manual = st.text_input("Escreva manualmente se não encontrou:")
        if st.button("Enviar Pedido Manual"):
            if manual:
                requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": manual})
                st.warning("O seu pedido foi enviado, mas nem todas as músicas estão disponíveis em Karaoke.")

    with col2:
        st.subheader("📸 Foto")
        st.camera_input("")
        if st.button("Sair / Limpar Registo"):
            st.session_state.registado = False
            st.rerun()
