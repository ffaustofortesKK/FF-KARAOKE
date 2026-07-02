import streamlit as st
import requests

# --- CONFIGURAÇÕES ---
st.set_page_config(page_title="FF KARAOKE CLOUD", layout="wide")

# --- CSS E ESTILOS ---
st.markdown("""
    <style>
    /* Logotipo completo e responsivo */
    .logo-container { width: 100%; display: flex; justify-content: center; margin-bottom: 20px; }
    .logo-container img { width: 100%; max-width: 500px; height: auto; object-fit: contain; }
    
    /* Texto branco com sombra para leitura em fundo escuro */
    .stApp, label, p, div, .stCheckbox { 
        color: white !important; 
        text-shadow: 1px 1px 2px #000; 
    }
    
    /* Input e Selectbox com texto branco e sombra */
    input, div[data-baseweb="select"] { 
        color: white !important; 
        text-shadow: 1px 1px 2px #000;
        background-color: #1a1a1a !important; 
        border: 2px solid #D4AF37 !important; 
    }
    
    /* Texto Bem-vindo: Amarelo, Negrito e Maior */
    .welcome-text { 
        color: #FFD700 !important; 
        font-weight: bold; 
        font-size: 28px !important;
        text-shadow: 2px 2px 4px #000;
        margin-bottom: 15px;
    }
    
    /* Botões */
    div.stButton > button { background-color: #D4AF37 !important; color: #000 !important; font-weight: bold; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# --- ESTADO DA SESSÃO ---
if 'registado' not in st.session_state: st.session_state.registado = False
if 'resultados_busca' not in st.session_state: st.session_state.resultados_busca = None

# --- CABEÇALHO ---
st.markdown('<div class="logo-container"><img src="https://i.ibb.co/HfKTnDDQ/logoweb.png"></div>', unsafe_allow_html=True)

# --- LÓGICA DA INTERFACE ---
if not st.session_state.registado:
    st.subheader("📝 Registo Inicial")
    nome = st.text_input("Nome:")
    st.markdown("[👉 Seguir no TikTok](https://www.tiktok.com/@ff_karaoke) | [👉 Seguir no Instagram](https://www.instagram.com/ff.karaoke/)")
    check_social = st.checkbox("Confirmo que segui o Grupo FF nas Redes Sociais")
    
    if st.button("Concluir Registo"):
        if nome and check_social:
            st.session_state.nome = nome
            st.session_state.registado = True
            st.rerun()
        else:
            st.error("Preencha o nome e confirme as redes sociais!")
else:
    # Texto de Bem-vindo estilizado
    st.markdown(f'<p class="welcome-text">Bem-vindo, {st.session_state.nome}!</p>', unsafe_allow_html=True)
    
    # Campo de busca
    busca = st.text_input("Título / Cantor:")
    if st.button("Pesquisar"):
        # Aqui a sua lógica de busca Firebase...
        # Exemplo: st.session_state.resultados_busca = ['Musica 1', 'Musica 2']
        st.rerun()

    # Se houver resultados, mostra o select
    if st.session_state.resultados_busca:
        escolha = st.selectbox("Selecione a música:", st.session_state.resultados_busca, key="select_m")
        
        if st.button("Confirmar Pedido"):
            # Lógica de POST para o Firebase...
            st.success(f"Pedido de {escolha} enviado com sucesso!")
            
            # EFEITOS: Confetti/Fogo de artifício
            st.balloons()
            
            # Limpa o estado da seleção
            st.session_state.resultados_busca = None
            st.rerun()
