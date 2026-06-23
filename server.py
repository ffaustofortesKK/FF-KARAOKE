import streamlit as st
import json
import os

# Configuração da página do Streamlit
st.set_page_config(page_title="FF KARAOKE - Pedir Música", page_icon="🎤", layout="centered")

# Nome do ficheiro partilhado na nuvem para romper o isolamento de sessão
FICHEIRO_NUVEM = "ultimo_pedido_stream.txt"

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

# --- INTERCEÇÃO DA API (O que o computador lê) ---
query_params = st.query_params
if "api" in query_params:
    if os.path.exists(FICHEIRO_NUVEM):
        with open(FICHEIRO_NUVEM, "r", encoding="utf-8") as f:
            conteudo = f.read().strip()
            if conteudo:
                st.text(conteudo)
                st.stop()
    
    # Se o ficheiro não existir ou estiver vazio, devolve estrutura vazia
    st.text(json.dumps({"cantor": "", "musica": ""}))
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
        dados_pedido = {
            "cantor": nome_cantor.strip(),
            "musica": nome_musica.strip()
        }
        # Grava no ficheiro partilhado que ignora o bloqueio de utilizadores do Streamlit
        with open(FICHEIRO_NUVEM, "w", encoding="utf-8") as f:
            f.write(json.dumps(dados_pedido))
            
        st.success(f"✅ Sucesso, {nome_cantor}! O teu pedido foi enviado para o painel do operador.")
        st.balloons()

# Mostrar na tela do telemóvel para confirmação visual
if os.path.exists(FICHEIRO_NUVEM):
    try:
        with open(FICHEIRO_NUVEM, "r", encoding="utf-8") as f:
            print_dados = json.loads(f.read())
            if print_dados.get("cantor"):
                st.write("---")
                st.caption(f"🎤 Último pedido registado no sistema: {print_dados['cantor']} — {print_dados['musica']}")
    except: pass
