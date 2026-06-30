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
@st.cache_data(ttl=60)
def carregar_catalogo_real():
    nome_arquivo = "musicas.txt"
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            return [linha.strip() for linha in f.readlines() if linha.strip()]
    else:
        # Lista padrão de segurança caso o arquivo ainda não esteja no servidor
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
# OPERAÇÃO EM PASSO A PASSO
# =========================================================

# 1º Nome do Cantor
cantor = st.text_input("1º Nome do Cantor (Seu Nome):", placeholder="Ex: Fausto Fortes")

# 2º Pesquisar Música
busca_musica = st.text_input("2º Pesquisar Música (Digite o nome da música ou artista):", placeholder="Ex: Paulo Flores").strip()

# Variáveis de controlo
musica_final = ""
modo_manual = False

if busca_musica:
    # Filtra o catálogo procurando o que o utilizador digitou
    resultados = [m for m in catalogo_musicas if busca_musica.lower() in m.lower()]
    
    if resultados:
        st.markdown("⬇️ **Músicas encontradas na sua nuvem MEGA. Selecione a desejada:**")
        musica_final = st.selectbox("Escolha a versão exata:", resultados, key="selecao_resultado")
    else:
        # Se NÃO encontrar nenhuma correspondência na nuvem
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
        st.error("⚠️ Por favor, digite o seu nome no **1º campo** antes de enviar.")
    elif not busca_musica:
        st.error("⚠️ Por favor, pesquise e selecione uma música no **2º campo**.")
    else:
        dados = {
            "cantor": cantor.strip(),
            "musica": musica_final.strip()
        }
        
        try:
            resposta = requests.post(URL_FIREBASE, data=json.dumps(dados), timeout=5)
            if resposta.status_code == 200:
                if modo_manual:
                    # Alerta customizado para pedidos manuais fora do catálogo
                    st.warning("⚠️ Seu pedido foi enviado, mas não temos a certeza que ela esteja disponível em Karaoke.")
                else:
                    # Sucesso normal para músicas confirmadas na nuvem
                    st.success(f"🎉 Perfeito! Pedido de **{dados['musica']}** enviado com sucesso para a fila!")
                    st.balloons()
            else:
                st.error("❌ Erro ao processar o pedido. Tente novamente.")
        except Exception as e:
            st.error(f"Erro de comunicação com o Firebase: {e}")
