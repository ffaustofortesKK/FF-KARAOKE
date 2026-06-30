import streamlit as st
import requests
import json
import os

# --- CONFIGURAÇÕES ---
URL_FIREBASE = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"

# Configuração da página
st.set_page_config(page_title="FF Karaoke Cloud", page_icon="🎤", layout="centered")

st.title("🎤 FF KARAOKE CLOUD")
st.write("Preencha os campos na ordem abaixo para enviar o seu pedido:")
st.write("---")

# --- FUNÇÃO PARA CARREGAR AS MÚSICAS DO SEU MEGA ---
@st.cache_data(ttl=60) # Atualiza a lista a cada 1 minuto se o arquivo mudar
def carregar_catalogo_real():
    nome_arquivo = "musicas.txt"
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            return [linha.strip() for linha in f.readlines() if linha.strip()]
    else:
        # Se o musicas.txt não for encontrado no servidor, avisa o administrador
        return []

# Inicializa o catálogo do MEGA
catalogo_musicas = carregar_catalogo_real()

# Alerta caso o arquivo musicas.txt não tenha sido enviado para o servidor ainda
if not catalogo_musicas:
    st.info("ℹ️ Modo de digitação livre ativo. (Crie o arquivo 'musicas.txt' no servidor para ativar o catálogo automático).")

# =========================================================
# OPERAÇÃO EM PASSO A PASSO (FLUXO EM ABA ÚNICA)
# =========================================================

# 1º Nome do Cantor
cantor = st.text_input("1º Nome do Cantor (Seu Nome):", placeholder="Ex: Fausto Fortes")

# 2º Pesquisar Música
busca_musica = st.text_input("2º Pesquisar Música (Digite o nome da música, cantor ou link do MEGA):", placeholder="Ex: Paulo Flores ou cole o link").strip()

# Variável para guardar o que vai para o DJ
musica_final = ""

if busca_musica:
    if catalogo_musicas:
        # Filtra procurando o termo ou link digitado
        resultados = [m for m in catalogo_musicas if busca_musica.lower() in m.lower()]
        
        if resultados:
            st.markdown("⬇️ **Músicas encontradas na sua nuvem MEGA. Selecione a desejada:**")
            musica_final = st.selectbox("Escolha a versão exata:", resultados, key="selecao_resultado")
        else:
            st.warning("⚠️ Esta música não consta na lista pré-carregada do MEGA.")
            st.info("Pode enviar o pedido assim mesmo. O sistema aceitará o que digitou.")
            musica_final = busca_musica
    else:
        # Se não há catálogo enviado, aceita diretamente o que foi digitao (ex: o link)
        musica_final = busca_musica
else:
    musica_final = ""

st.write("---")

# 3º Enviar pedido
btn_enviar = st.button("3º Enviar Pedido 🚀", use_container_width=True)

# --- PROCESSAMENTO DO ENVIO ---
if btn_enviar:
    if not cantor:
        st.error("⚠️ Por favor, digite o seu nome no **1º campo** antes de enviar.")
    elif not busca_musica:
        st.error("⚠️ Por favor, preencha o **2º campo** com a música ou link.")
    else:
        dados = {
            "cantor": cantor.strip(),
            "musica": musica_final.strip() if musica_final else busca_musica.strip()
        }
        
        try:
            resposta = requests.post(URL_FIREBASE, data=json.dumps(dados), timeout=5)
            if resposta.status_code == 200:
                st.success(f"🎉 Perfeito! Pedido enviado com sucesso para a fila!")
                st.balloons()
            else:
                st.error("❌ Erro ao processar o pedido. Tente novamente.")
        except Exception as e:
            st.error(f"Erro de comunicação com o Firebase: {e}")
