import streamlit as st
import requests

# ... (Configurações de URL mantêm-se iguais)

# --- CSS PERSONALIZADO ---
st.markdown("""
    <style>
    /* ... (Restante do CSS) ... */

    /* Por cor branca aos labels indicados na gfdsa.png */
    label { color: white !important; }

    /* Estilo para o aviso de sucesso conforme solicitado */
    .success-box {
        background-color: #008000;
        color: black;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ... (Dentro da lógica do código)

    # 1. Pesquisa (removi o st.error que gerava o retângulo vermelho)
    if st.button("Pesquisar"):
        try:
            resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
            # ... (Lógica de busca)
        except:
            # Em vez de st.error (que cria o retângulo vermelho), usamos apenas um log ou nada
            pass 

    # 2. Confirmação do Pedido com texto de sucesso abaixo
    if 'resultados' in st.session_state and st.session_state.resultados:
        escolha = st.selectbox("Selecione a música:", st.session_state.resultados)
        if st.button("Confirmar Pedido"):
            requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": escolha})
            
            # Texto de sucesso conforme a imagem gfdsa.png
            st.markdown('<div class="success-box">o seu pedido foi enviado com sucesso</div>', unsafe_allow_html=True)
            
            st.balloons()
            st.session_state.resultados = None
