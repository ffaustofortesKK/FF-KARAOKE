import streamlit as str
from sqlalchemy import text  
import json

# Configuração da página do telemóvel do cliente
str.set_page_config(page_title="FF KARAOKE - Pedir Música", page_icon="🎤", layout="centered")

# --- VERIFICAÇÃO DE API PARA O PC (SISTEMA INTEGRADO) ---
# Se o PC chamar o site com ?api=1, o site responde apenas os dados puros em JSON e para por aqui
query_params = str.query_params
if "api" in query_params and query_params["api"] == "1":
    try:
        conn = str.connection("pedidos_db", type="sql")
        df = conn.query("SELECT cantor, musica FROM karaoke_pedidos ORDER BY id DESC LIMIT 1;", ttl=0)
        if not df.empty:
            resposta = {
                "cantor": str(df['cantor'].iloc[0]),
                "musica": str(df['musica'].iloc[0])
            }
            str.text(json.dumps(resposta, ensure_ascii=False))
        else:
            str.text(json.dumps({}))
    except Exception as e:
        str.text(json.dumps({"erro": str(e)}))
    str.stop()  # Interrompe o resto da página para enviar só o dado puro ao PC

# Estilo visual personalizado (Cores do FF Karaoke)
str.markdown("""
    <style>
    .main { background-color: #111111; color: white; }
    h1 { color: #f1c40f; text-align: center; font-family: 'Arial', sans-serif; }
    .stButton>button { background-color: #f1c40f; color: black; font-weight: bold; width: 100%; }
    </style>
""", unsafe_allow_html=True)

str.markdown("<h1>🎤 FF KARAOKE CLOUD 🎵</h1>", unsafe_allow_html=True)
str.write("---")

# Liga à base de dados interna do Streamlit
conn = str.connection("pedidos_db", type="sql")

# Cria a tabela se não existir
with conn.session as session:
    session.execute(text("CREATE TABLE IF NOT EXISTS karaoke_pedidos (id INTEGER PRIMARY KEY AUTOINCREMENT, cantor TEXT, musica TEXT);"))
    session.commit()

with str.form(key="form_pedido"):
    nome_cantor = str.text_input("Seu Nome (Quem vai cantar):", placeholder="Ex: Fausto Fortes")
    nome_musica = str.text_input("Nome da Música ou Artista:", placeholder="Ex: Vou Cantar Para Não Chorar")
    botao_enviar = str.form_submit_button(label="🚀 ENVIAR PEDIDO DE MÚSICA")

if botao_enviar:
    if nome_cantor.strip() == "" or nome_musica.strip() == "":
        str.error("❌ Por favor, preencha o seu nome e o nome da música!")
    else:
        with conn.session as session:
            session.execute(
                text("INSERT INTO karaoke_pedidos (cantor, musica) VALUES (:cantor, :musica);"),
                {"cantor": nome_cantor.strip(), "musica": nome_musica.strip()}
            )
            session.commit()
        str.success(f"✅ Sucesso, {nome_cantor}! O teu pedido foi enviado.")
        str.balloons()

# Mostra o último pedido na página de forma visual
df = conn.query("SELECT cantor, musica FROM karaoke_pedidos ORDER BY id DESC LIMIT 1;", ttl=0)
if not df.empty:
    str.info(f"🎤 Último pedido enviado: **{df['cantor'].iloc[0]}** — 🎵 **{df['musica'].iloc[0]}**")
