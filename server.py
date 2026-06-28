import streamlit as st
import requests
import json

URL_FIREBASE = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json" # Mudei para /pedidos (plural)

st.title("🎤 FF KARAOKE")

with st.form("form_pedido"):
    cantor = st.text_input("Nome do Cantor")
    musica = st.text_input("Nome da Música")
    # A foto tirada aqui precisa ser salva no Cloud Storage, 
    # não enviada via base64 para o Realtime Database.
    btn_enviar = st.form_submit_button("Enviar Pedido")

if btn_enviar and cantor and musica:
    # AVISO: Sem o Firebase Storage, você não conseguirá exibir a foto real
    # Recomendação: Peça apenas o nome do cantor e música por enquanto
    dados = {"cantor": cantor, "musica": musica}
    
    # Use POST em vez de PUT para criar uma fila e não sobrescrever
    resposta = requests.post(URL_FIREBASE, data=json.dumps(dados))
    
    if resposta.status_code == 200:
        st.success("Pedido enviado com sucesso!")
    else:
        st.error("Erro ao enviar.")
