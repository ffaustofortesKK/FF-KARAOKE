import streamlit as st
import requests

# --- CONFIGURAÇÕES ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"

st.set_page_config(page_title="FF KARAOKE CLOUD", layout="wide")

# CSS para a Lupa e estilo geral
st.markdown("""
    <style>
    .stApp { background: #090A0F; color: white; }
    .search-icon { font-size: 24px; margin-right: 10px; }
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
    st.markdown("### <span class='search-icon'>🔍</span> Pesquisar Música", unsafe_allow_html=True)
    busca = st.text_input("", placeholder="Digite o nome da música...")
    
    escolha = None
    if busca:
        try:
            resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
            dados = resp.json()
            cat = list(dados.keys()) if isinstance(dados, dict) else dados
            resultados = [m for m in cat if busca.lower() in m.lower()]
            if resultados:
                escolha = st.selectbox("Selecione:", resultados)
        except: 
            st.error("Erro ao conectar ao catálogo.")

    # --- ENVIO ---
    if escolha:
        st.write(f"Música selecionada: **{escolha}**")
        
        if st.button("Confirmar Pedido"):
            payload = {
                "cantor": st.session_state.nome, 
                "musica": escolha,
                "foto": None # Foto removida conforme solicitado
            }
            requests.post(URL_FIREBASE_PEDIDOS, json=payload)
            
            # Efeito de Palmas
            st.success("Pedido enviado com sucesso!")
            st.balloons()
            
            # Tocar som de palmas (Certifique-se de ter um arquivo 'palmas.mp3' na pasta)
            try:
                st.audio("https://www.myinstants.com/media/sounds/applause.mp3", format="audio/mp3", autoplay=True)
            except:
                pass

    if st.button("Sair"):
        st.session_state.registado = False
        st.rerun()
