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
@st.cache_data(ttl=3600)
def carregar_catalogo_real():
    nome_arquivo = "musicas.txt"
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            return [linha.strip() for line in f.readlines() if line.strip()]
    else:
        # Lista de teste caso o musicas.txt não esteja na pasta ainda
        return [
            "Paulo Flores - Garina",
            "Paulo Flores - Poema do Semba",
            "Paulo Flores & Yuri da Cunha - Njila Ya Dikanga",
            "Fausto Fortes - Vou Cantar Para Não Chorar",
            "Bonga - Olhos Molhados"
        ]

# Inicializa o catálogo do MEGA
catalogo_musicas = carregar_catalogo_real()

# =========================================================
# OPERAÇÃO EM PASSO A PASSO (FLUXO EM ABA ÚNICA)
# =========================================================

# 1º Nome do Cantor
cantor = st.text_input("1º Nome do Cantor (Seu Nome):", placeholder="Ex: Fausto Fortes")

# 2º Pesquisar Música
busca_musica = st.text_input("2º Pesquisar Música (Digite o nome da música ou artista):", placeholder="Ex: Paulo Flores").strip()

# Variável para guardar o que vai para o DJ
musica_final = ""

if busca_musica:
    # Filtra o catálogo do MEGA procurando o que o utilizador digitou
    resultados = [m for m in catalogo_musicas if busca_musica.lower() in m.lower()]
    
    if resultados:
        st.markdown("⬇️ **Músicas encontradas na sua nuvem MEGA. Selecione a desejada:**")
        # Cria a lista de escolha com as opções encontradas
        musica_final = st.selectbox("Escolha a versão exata:", resultados, key="selecao_resultado")
    else:
        st.error("❌ Nenhuma música encontrada com esse nome no acervo do MEGA.")
        st.info("Nota: Pode avançar e enviar o pedido assim mesmo se o DJ tiver o ficheiro local.")
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
        st.error("⚠️ Por favor, pesquise e selecione uma música no **2º campo**.")
    else:
        # Envia os dados limpos para o Firebase
        dados = {
            "cantor": cantor.strip(),
            "musica": musica_final.strip() if musica_final else busca_musica.strip()
        }
        
        try:
            # Correção do nome da variável aqui (de resposta para resposta)
            resposta = requests.post(URL_FIREBASE, data=json.dumps(dados), timeout=5)
            if resposta.status_code == 200:
                st.success(f"🎉 Perfeito! Pedido de **{dados['musica']}** enviado com sucesso para a fila!")
                st.balloons() # Animação de balões no ecrã
            else:
                st.error("❌ Erro ao processar o pedido. Tente novamente.")
        except Exception as e:
            st.error(f"Erro de comunicação com o Firebase: {e}")
