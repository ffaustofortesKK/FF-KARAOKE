import streamlit as st
import requests
import json
import base64
from io import BytesIO

URL_FIREBASE = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedido.json"

st.title("🎤 FF KARAOKE")

with st.form("form_pedido"):
    cantor = st.text_input("Nome do Cantor")
    musica = st.text_input("Nome da Música")
    foto = st.camera_input("Tirar foto para o palco") # Tira a foto pelo telemóvel
    btn_enviar = st.form_submit_button("Enviar Pedido")

if btn_enviar and cantor and musica:
    foto_base64 = ""
    if foto:
        # Converte a imagem para bytes e depois para base64 para enviar como texto
        bytes_data = foto.getvalue()
        foto_base64 = base64.b64encode(bytes_data).decode('utf-8')
    
    dados = {"cantor": cantor, "musica": musica, "foto": foto_base64}
    requests.put(URL_FIREBASE, data=json.dumps(dados))
    st.success("Pedido enviado!")
