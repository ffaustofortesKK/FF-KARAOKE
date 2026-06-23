import streamlit as st
import requests
import json

# Configuração da página do Streamlit
st.set_page_config(page_title="FF KARAOKE - Pedir Música", page_icon="🎤", layout="centered")

# Estilo visual personalizado (Tema Escuro e Dourado)
st.markdown("""
    <style>
    .main { background-color: #111111; color: white; }
    h1 { color: #f1c40f; text-align: center; font-family: 'Arial', sans-serif; margin-bottom: 0px; }
    .subtitulo { color: #aaaaaa; text-align: center; font-size: 14px; margin-bottom: 20px; }
    .stButton>button { background-color: #f1c40f; color: black; font-weight: bold; width: 100%; border-radius: 8px; height: 50px; font-size: 16px; border: none; }
    .stButton>button:hover { background-color: #fff200; color: black; }
    div.stTextInput>div>div>input { background-color: #222222; color: white; border: 1px solid #333333; }
    div.stTextInput>div>div>input:focus { border-color: #f1c40f; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🎤 FF KARAOKE CLOUD 🎵</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitulo'>Escolha a sua música e solte a sua voz!</p>", unsafe_allow_html=True)
st.write("---")

# Inicializa um histórico temporário na memória do Streamlit para evitar falhas de leitura
if "ultimo_pedido" not in st.session_state:
    st.session_state["ultimo_pedido"] = {"cantor": "", "musica": ""}

# --- INSTALAÇÃO DA API: Envia os dados para o app.py do computador ---
query_params = st.query_params
if "api" in query_params:
    # Entrega o último pedido feito em formato JSON limpo para o PC ler
    st.text(json.dumps(st.session_state["ultimo_pedido"]))
    st.stop()

# --- FORMULÁRIO PARA OS CLIENTES (TELEMÓVEL) ---
with st.form(key="form_pedido"):
    nome_cantor = st.text_input("Seu Nome (Quem vai cantar):", placeholder="Ex: Fausto Fortes")
    nome_musica = st.text_input("Nome da Música ou Artista:", placeholder="Ex: Melodia da Saudade")
    botao_enviar = st.form_submit_button(label="🚀 ENVIAR PEDIDO DE MÚSICA")

# Processamento do envio do formulário
if botao_enviar:
    if nome_cantor.strip() == "" or nome_musica.strip() == "":
        st.error("❌ Por favor, preencha o seu nome e o nome da música!")
    else:
        # Atualiza o pedido na nuvem
        st.session_state["ultimo_pedido"] = {
            "cantor": nome_cantor.strip(),
            "musica": nome_musica.strip()
        }
        st.success(f"✅ Sucesso, {nome_cantor}! O teu pedido foi enviado para o painel do operador.")
        st.balloons()

# Rodapé informativo
if st.session_state["ultimo_pedido"]["cantor"] != "":
    st.write("---")
    st.caption(f"🎤 Último pedido registado: {st.session_state['ultimo_pedido']['cantor']} — {st.session_state['ultimo_pedido']['musica']}")
