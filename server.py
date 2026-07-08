import streamlit as st
import requests
import base64

# --- CONFIGURAÇÕES ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"
LINK_LOGO = "https://cdn.phototourl.com/free/2026-07-03-793a0f18-6143-44c8-b56e-e44af828c30c.png"
# Som de palmas (pode substituir por outro link direto de mp3)
URL_SOM_PALMAS = "https://www.soundjay.com/buttons/sounds/button-10.mp3"

st.set_page_config(page_title="FF KARAOKE CLOUD", layout="wide")

# CSS personalizado com o Logotipo no fundo
st.markdown(f"""
    <style>
    .stApp {{ 
        background: linear-gradient(rgba(9, 10, 15, 0.85), rgba(9, 10, 15, 0.85)), url('{LINK_LOGO}');
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
    
    # BUSCA COM LUPA
    busca = st.text_input("🔍 Pesquisar Música:")
    
    escolha = None
    if busca:
        try:
            resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
            dados = resp.json()
            cat = list(dados.keys()) if isinstance(dados, dict) else dados
            resultados = [m for m in cat if busca.lower() in m.lower()]
            escolha = st.selectbox("Selecione:", resultados)
        except: escolha = None
    
    # --- ENVIO ---
    if escolha:
        st.write(f"Música selecionada: **{escolha}**")
        
        # Botões lado a lado
        col1, col2 = st.columns([1, 6])
        
        with col1:
            if st.button("Confirmar Pedido"):
                payload = {
                    "cantor": st.session_state.nome, 
                    "musica": escolha,
                    "foto": None
                }
                requests.post(URL_FIREBASE_PEDIDOS, json=payload)
                
                # Som de palmas e feedback
                st.audio(URL_SOM_PALMAS, autoplay=True)
                st.success("Pedido enviado com sucesso!")
                st.balloons()
                
                # Limpa os campos após o envio
                st.rerun()
        
        with col2:
            if st.button("Limpar"):
                st.success("Campos limpos!")
                st.rerun()

    st.divider()
    if st.button("Sair"):
        st.session_state.registado = False
        st.rerun()
