import streamlit as st
import requests

# Configurações de página
st.set_page_config(page_title="FF KARAOKE CLOUD", layout="wide")

st.markdown("""
    <style>
    /* Logotipo completo */
    .logo-container { width: 100%; display: flex; justify-content: center; margin-bottom: 20px; }
    .logo-container img { width: 100%; max-width: 500px; height: auto; object-fit: contain; }
    
    /* Texto branco com sombra */
    .stApp, label, p, div { color: white !important; text-shadow: 1px 1px 2px #000; }
    
    /* Texto Bem-vindo Amarelo e Negrito */
    .welcome-text { color: #FFD700 !important; font-weight: bold; font-size: 24px; }
    
    /* Inputs */
    div[data-baseweb="input"] > div { background-color: #1a1a1a !important; border: 2px solid #D4AF37 !important; }
    div.stButton > button { background-color: #D4AF37 !important; color: #000 !important; font-weight: bold; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# Lógica de Estado
if 'registado' not in st.session_state: st.session_state.registado = False
if 'resultados_busca' not in st.session_state: st.session_state.resultados_busca = None

st.markdown('<div class="logo-container"><img src="https://i.ibb.co/HfKTnDDQ/logoweb.png"></div>', unsafe_allow_html=True)

if not st.session_state.registado:
    nome = st.text_input("Nome:")
    st.markdown("[👉 Seguir no TikTok](https://www.tiktok.com/@ff_karaoke) | [👉 Seguir no Instagram](https://www.instagram.com/ff.karaoke/)")
    check_social = st.checkbox("Confirmo que segui o Grupo FF nas Redes Sociais")
    
    if st.button("Concluir Registo"):
        if nome and check_social:
            st.session_state.nome = nome
            st.session_state.registado = True
            st.rerun()
else:
    st.markdown(f'<p class="welcome-text">Bem-vindo, {st.session_state.nome}!</p>', unsafe_allow_html=True)
    
    busca = st.text_input("Título / Cantor:")
    if st.button("Pesquisar"):
        # (Lógica de busca aqui como anterior)
        st.session_state.resultados_busca = ["Exemplo Música 1", "Exemplo Música 2"] # Exemplo
        st.rerun()

    if st.session_state.resultados_busca:
        escolha = st.selectbox("Selecione a música:", st.session_state.resultados_busca, key="select_musica")
        if st.button("Confirmar Pedido"):
            # Enviar para Firebase...
            st.success(f"Pedido de {escolha} enviado!")
            st.balloons() # Fogo de artifício
            st.session_state.resultados_busca = None # Limpa a lista
            st.rerun()
