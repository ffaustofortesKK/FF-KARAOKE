import streamlit as st
import json
from sqlalchemy import text

# =========================================================================
# 1. API DE RESPOSTA AO PORTÁTIL (Sem Cache)
# =========================================================================
query_params = st.query_params

if "obter_pedido" in query_params:
    try:
        conn = st.connection("pedidos_db", type="sql")
        df = conn.query("SELECT cantor, musica FROM karaoke_pedidos ORDER BY id DESC LIMIT 1;", ttl=0)
        
        if not df.empty:
            resposta = {"cantor": str(df['cantor'].iloc[0]), "musica": str(df['musica'].iloc[0])}
        else:
            resposta = {"cantor": "", "musica": ""}
    except Exception as e:
        resposta = {"cantor": "Erro BD", "musica": str(e)}
    
    st.text(json.dumps(resposta, ensure_ascii=False))
    st.stop()

# =========================================================================
# 2. DESIGN DA INTERFACE PARA OS CLIENTES (Telemóvel)
# =========================================================================
st.set_page_config(page_title="FF KARAOKE - Pedir Música", page_icon="🎤", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #111111; color: white; }
    h1 { color: #f1c40f; text-align: center; font-family: 'Arial', sans-serif; }
    .stButton>button { background-color: #f1c40f; color: black; font-weight: bold; width: 100%; height: 3em; border-radius: 10px; }
    .stButton>button:hover { background-color: #fff200; color: black; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🎤 FF KARAOKE CLOUD 🎵</h1>", unsafe_allow_html=True)
st.write("---")

# Inicializa a Base de Dados SQL interna do Streamlit
conn = st.connection("pedidos_db", type="sql")
with conn.session as session:
    session.execute(text("CREATE TABLE IF NOT EXISTS karaoke_pedidos (id INTEGER PRIMARY KEY AUTOINCREMENT, cantor TEXT, musica TEXT);"))
    session.commit()

# Formulário de envio
with st.form(key="form_pedido", clear_on_submit=True):
    nome_cantor = st.text_input("Seu Nome (Quem vai cantar):", placeholder="Ex: Fausto Fortes")
    nome_musica = st.text_input("Nome da Música ou Artista:", placeholder="Ex: Vou Cantar Para Não Chorar")
    botao_enviar = st.form_submit_button(label="🚀 ENVIAR PEDIDO DE MÚSICA")

if botao_enviar:
    if nome_cantor.strip() == "" or nome_musica.strip() == "":
        st.error("❌ Por favor, preencha o seu nome e o nome da música!")
    else:
        try:
            with conn.session as session:
                session.execute(
                    text("INSERT INTO karaoke_pedidos (cantor, musica) VALUES (:cantor, :musica);"),
                    {"cantor": nome_cantor.strip(), "musica": nome_musica.strip()}
                )
                session.commit()
            st.success(f"✅ Sucesso, {nome_cantor}! O teu pedido foi enviado.")
            st.balloons()
        except:
            st.error("Erro ao guardar o pedido na Base de Dados.")
