import streamlit as st
import requests
import json

# --- CONFIGURAÇÕES ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"

# Configuração da página
st.set_page_config(page_title="FF Karaoke Cloud", page_icon="🎤", layout="centered")

st.title("🎤 FF KARAOKE CLOUD")
st.write("Preencha os campos na ordem abaixo para enviar o seu pedido:")
st.write("---")

# --- FUNÇÃO PARA CARREGAR AS MÚSICAS DIRETO DO FIREBASE ---
@st.cache_data(ttl=300) 
def carregar_catalogo_firebase():
    try:
        resposta = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
        if resposta.status_code == 200 and resposta.json():
            return resposta.json()
    except:
        pass
    return [
        "Paulo Flores - Garina",
        "Paulo Flores - Poema do Semba",
        "Fausto Fortes - Vou Cantar Para Não Chorar",
        "Bonga - Olhos Molhados"
    ]

catalogo_musicas = carregar_catalogo_firebase()

# =========================================================
# OPERAÇÃO EM PASSO A PASSO
# =========================================================

# 1º Nome do Cantor
cantor = st.text_input("1º Nome do Cantor (Seu Nome):", placeholder="Ex: Fausto Fortes")

# --- NOVA FUNCIONALIDADE: SELFIE ---
st.write("---")
st.subheader("📸 Tirar Selfie (Opcional)")
foto_selfie = st.camera_input("Tire uma foto para o seu perfil")

if foto_selfie:
    st.success("Foto capturada com sucesso!")
st.write("---")

# 2º Pesquisar Música
busca_musica = st.text_input("2º Pesquisar Música (Digite o nome da música ou artista):", placeholder="Ex: Paulo Flores").strip()

# Variáveis de controlo
musica_final = ""
modo_manual = False

if busca_musica:
    resultados = [m for m in catalogo_musicas if busca_musica.lower() in m.lower()]
    
    if resultados:
        st.markdown("⬇ *Músicas encontradas na sua nuvem. Selecione a desejada:*")
        musica_final = st.selectbox("Escolha a versão exata:", resultados, key="selecao_resultado")
    else:
        st.error("❌ Essa música não está disponível no nosso acervo da nuvem MEGA.")
        modo_manual = True
        st.write("---")
        st.subheader("📝 Pedido Manual")
        pedido_manual = st.text_input("Introduza o nome da música desejada para verificação do DJ:", value=busca_musica)
        musica_final = pedido_manual

st.write("---")

# 3º Enviar pedido
btn_enviar = st.button("3º Enviar Pedido 🚀", use_container_width=True)

# --- PROCESSAMENTO DO ENVIO ---
if btn_enviar:
    if not cantor:
        st.error("⚠️ Por favor, digite o seu nome no 1º campo antes de enviar.")
    elif not busca_musica:
        st.error("⚠️ Por favor, pesquise e selecione uma música no 2º campo.")
    else:
        # A foto é guardada na variável 'foto_selfie'
        # Se quiseres enviar a foto para o Firebase, terias de a converter para base64.
        # Por agora, ela está disponível para exibição imediata se necessário.
        
        dados = {
            "cantor": cantor.strip(),
            "musica": musica_final.strip(),
            "tem_foto": True if foto_selfie else False
        }
        
        try:
            resposta = requests.post(URL_FIREBASE_PEDIDOS, data=json.dumps(dados), timeout=5)
            if resposta.status_code == 200:
                if modo_manual:
                    st.warning("⚠️ Seu pedido foi enviado, mas não temos a certeza que ela esteja disponível em Karaoke.")
                else:
                    st.success(f"🎉 Perfeito! Pedido de **{dados['musica']}** enviado com sucesso para a fila!")
                    st.balloons()
            else:
                st.error("❌ Erro ao processar o pedido. Tente novamente.")
        except Exception as e:
            st.error(f"Erro de comunicação com o Firebase: {e}")
