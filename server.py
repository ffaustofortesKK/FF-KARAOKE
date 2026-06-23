import streamlit as st
from sqlalchemy import text
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

# Liga à base de dados interna (SQLite integrada no Streamlit)
conn = st.connection("pedidos_db", type="sql")

# Garante que a tabela de pedidos existe
with conn.session as session:
    session.execute(text("CREATE TABLE IF NOT EXISTS karaoke_pedidos (id INTEGER PRIMARY KEY AUTOINCREMENT, cantor TEXT, musica TEXT);"))
    session.commit()

# --- INSTALAÇÃO DA API: Verifica se o app.py do PC está a pedir dados ---
query_params = st.query_params
if "api" in query_params:
    # Puxa o último pedido feito na base de dados
    df = conn.query("SELECT cantor, musica FROM karaoke_pedidos ORDER BY id DESC LIMIT 1;", ttl=0)
    
    if not df.empty:
        resposta = {
            "cantor": str(df['cantor'].iloc[0]), 
            "musica": str(df['musica'].iloc[0])
        }
    else:
        resposta = {"cantor": "", "musica": ""}
    
    # Entrega o resultado como JSON puro e para o Streamlit imediatamente
    st.text(json.dumps(resposta))
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
        try:
            with conn.session as session:
                session.execute(
                    text("INSERT INTO karaoke_pedidos (cantor, musica) VALUES (:cantor, :musica);"),
                    {"cantor": nome_cantor.strip(),  "musica": nome_musica.strip()}
                )
                session.commit()
            st.success(f"✅ Sucesso, {nome_cantor}! O teu pedido foi enviado para o operador.")
            st.balloons()  # Solta balões de comemoração no telemóvel
        except:
            st.error("❌ Erro temporário ao enviar o pedido. Tente novamente.")

# Espaço decorativo/informativo no rodapé do telemóvel
st.write("---")
df_visual = conn.query("SELECT cantor, musica FROM karaoke_pedidos ORDER BY id DESC LIMIT 1;", ttl=0)
if not df_visual.empty:
    st.caption(f"🎤 Último pedido enviado ao sistema: {df_visual['cantor'].iloc[0]} — {df_visual['musica'].iloc[0]}")
