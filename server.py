import streamlit as st
import requests
import json

# URL do seu Firebase (o final deve ser .json)
URL_FIREBASE = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedido.json"

st.set_page_config(page_title="FF KARAOKE - Pedidos", page_icon="🎤")

st.title("🎤 FF KARAOKE - Pedir Música")

with st.form("form_pedido"):
    cantor = st.text_input("Nome do Cantor/Grupo")
    musica = st.text_input("Nome da Música")
    mensagem = st.text_area("Mensagem (Opcional)")
    
    btn_enviar = st.form_submit_button("Enviar Pedido")

if btn_enviar:
    if cantor and musica:
        dados = {
            "cantor": cantor,
            "musica": musica,
            "mensagem": mensagem
        }
        
        # Envia os dados para o Firebase (usamos PUT para sobrescrever o pedido atual)
        try:
            resposta = requests.put(URL_FIREBASE, data=json.dumps(dados))
            if resposta.status_code == 200:
                st.success("✅ Pedido enviado com sucesso! Aguarde a sua vez.")
            else:
                st.error("❌ Erro ao conectar com o sistema. Tente novamente.")
        except Exception as e:
            st.error(f"Erro: {e}")
    else:
        st.warning("⚠️ Por favor, preencha o Nome e a Música.")
