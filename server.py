import streamlit as st
import requests
import base64

# --- CONFIGURAÇÕES ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"
LINK_LOGO = "https://cdn.phototourl.com/free/2026-07-03-793a0f18-6143-44c8-b56e-e44af828c30c.png"
# Som de palmas (URL direta para o arquivo de áudio)
URL_SOM_PALMAS = "https://www.soundjay.com/buttons/sounds/button-10.mp3" 

st.set_page_config(page_title="FF KARAOKE CLOUD", layout="wide")

# CSS personalizado: Fundo com logo e estilo geral
st.markdown(f"""
    <style>
    .stApp {{ 
        background: linear-gradient(rgba(9, 10, 15, 0.9), rgba(9, 10, 15, 0.9)), url('{LINK_LOGO}');
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        color: white;
    }}
    </style>
""", unsafe_allow_html=True)

if 'registado' not in st.session_state: st.session_state.registado = False

if not st.session_state.registado:
    st.subheader("📝 Registo Inicial")
    nome = st.text_input("Nome:")
    if st.button("Concluir Registo"):
        if nome:
            st.session_state.nome = nome
            st.session_state.registado = True
            st.rerun()
else:
    st.title(f"Bem-vindo, {st.session_state.nome}!")
    
    # BUSCA COM ÍCONE DE LUPA
    busca = st.text_input("🔍 Pesquisar Música:")
    
    escolha = None
    if busca:
        try:
            resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
            dados = resp.json()
            cat = list(dados.keys()) if isinstance(dados, dict) else dados
            resultados = [m for m in cat if busca.lower() in m.lower()]
            escolha = st.selectbox("Selecione a música:", resultados)
        except: 
            st.error("Erro ao conectar ao catálogo.")

    # --- ENVIO ---
    if escolha:
        st.write(f"Música selecionada: **{escolha}**")
        
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("Confirmar Pedido"):
                payload = {
                    "cantor": st.session_state.nome, 
                    "musica": escolha,
                    "foto": None
                }
                requests.post(URL_FIREBASE_PEDIDOS, json=payload)
                
                # Efeito sonoro e feedback
                st.audio(URL_SOM_PALMAS, autoplay=True)
                st.success("Pedido enviado com sucesso!")
                st.balloons()
                
                # Limpa os campos através do rerun
                st.session_state.busca_feita = ""
                st.rerun()

        with col2:
            if st.button("Limpar"):
                st.success("Campos limpos!")
                st.rerun()

    st.divider()
    if st.button("Sair"):
        st.session_state.registado = False
        st.rerun()
