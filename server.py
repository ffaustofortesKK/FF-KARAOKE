import streamlit as st
import requests
import json
import os

# --- CONFIGURAÇÕES ---
URL_FIREBASE = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"

# Configuração da página
st.set_page_config(page_title="FF Karaoke Cloud", page_icon="🎤", layout="centered")

st.title("🎤 FF KARAOKE CLOUD")
st.write("Preencha os dados abaixo para enviar o seu pedido diretamente ao DJ!")

# --- FUNÇÃO PARA CARREGAR AS MÚSICAS DO SEU MEGA ---
@st.cache_data(ttl=3600)  # Guarda a lista na memória por 1 hora para o site voar!
def carregar_catalogo_real():
    nome_arquivo = "musicas.txt"
    # Se o arquivo com a lista do MEGA existir, ele lê. Se não, usa uma lista padrão.
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            return [linha.strip() for linha in f.readlines() if linha.strip()]
    else:
        # Fallback caso você ainda não tenha criado o musicas.txt
        return [
            "Fausto Fortes - Vou Cantar Para Não Chorar",
            "Bonga - Olhos Molhados",
            "Anselmo Ralph - Infelizmente",
            "Yola Semedo - Hipocrisia",
            "Matias Damásio - Como Antes"
        ]

# Inicializa o catálogo
catalogo_musicas = carregar_catalogo_real()

# --- FORMULÁRIO EM ABA ÚNICA ---
with st.form("form_karaoke_unico"):
    
    # 1º Nome do Cantor (Quem vai cantar no evento)
    cantor = st.text_input("1º Nome do Cantor (Seu Nome):", placeholder="Ex: Fausto Fortes")
    
    # 2º Pesquisar Música (Campo de busca integrado)
    busca_musica = st.text_input("2º Pesquisar Música (Digite o nome ou artista):", placeholder="Ex: Vou Cantar").strip()
    
    # Sistema de feedback visual em tempo real dentro do formulário
    musica_selecionada = ""
    if busca_musica:
        resultados = [m for m in catalogo_musicas if busca_musica.lower() in m.lower()]
        if resultados:
            st.markdown(f"**🟢 Encontradas no MEGA:**")
            # Cria uma caixa de seleção dinâmica com o que foi encontrado na nuvem
            musica_selecionada = st.selectbox("Escolha a música exata da lista:", resultados)
        else:
            st.markdown("**🔴 Música não encontrada no acervo do MEGA.**")
            st.caption("Você pode tentar enviar mesmo assim, mas confirme se o DJ possui o arquivo.")
            # Se não achar, assume o que o usuário digitou no campo de busca
            musica_selecionada = busca_musica
    
    # 3º Enviar pedido
    btn_enviar = st.form_submit_button("3º Enviar Pedido 🚀")

# --- PROCESSAMENTO DO ENVIO ---
if btn_enviar:
    if not cantor:
        st.error("⚠️ Por favor, digite o seu nome (1º campo) antes de enviar.")
    elif not busca_musica:
        st.error("⚠️ Por favor, pesquise e escolha uma música (2º campo) antes de enviar.")
    else:
        # Envia o nome de quem canta e a música final selecionada
        dados = {
            "cantor": cantor.strip(),
            "musica": musicas_selecionada if musica_selecionada else busca_musica.strip()
        }
        
        try:
            resposta = requests.post(URL_FIREBASE, data=json.dumps(dados), timeout=5)
            if respuesta.status_code == 200:
                st.success(f"🎉 Sucesso! Pedido de **{dados['musica']}** enviado para a fila do DJ!")
            else:
                st.error("❌ Erro ao processar o pedido na nuvem. Tente novamente.")
        except Exception as e:
            st.error(f"Erro de comunicação: {e}")
