import streamlit as st
import requests
import json
import time  # <--- Corrigido: Importação essencial adicionada!

# --- CONFIGURAÇÕES DO FIREBASE ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedido.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"

st.title("🎤 FF KARAOKE CLOUD")
st.subheader("Faz o teu pedido de música em tempo real!")

# 1. Procurar o catálogo atualizado no Firebase com tratamento de erro robusto
@st.cache_data(ttl=30)  # Atualiza a lista a cada 30 segundos
def carregar_catalogo():
    try:
        resposta = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
        if resposta.status_code == 200:
            dados = resposta.json()
            return dados if dados else {}
    except:
        pass
    return {}

catalogo = carregar_catalogo()

# Criar o formulário no site
with st.form("form_pedido"):
    nome_cliente = st.text_input("Teu Nome / Nome da Mesa:", placeholder="Ex: Fausto / Mesa 2")
    
    st.write("---")
    st.markdown("### 🎵 Escolha a sua Música")
    
    # Proteção contra o cache antigo: verifica se o catálogo veio como dicionário {} ou lista []
    if catalogo and isinstance(catalogo, dict):
        # Pega nos nomes limpos (chaves do dicionário)
        opcoes_musicas = list(catalogo.keys())
        
        musica_selecionada = st.selectbox(
            "Pesquise pelo Artista ou Nome da Música:",
            options=["-- Selecione uma música --"] + opcoes_musicas
        )
        
        musica_manual = ""
        if musica_selecionada == "-- Selecione uma música --":
            st.info("💡 Não encontras a tua música? Podes digitar o nome manualmente abaixo:")
            musica_manual = st.text_input("Digitar música manualmente (Artista - Título):")
            
    elif catalogo and isinstance(catalogo, list):
        # Caso o Firebase ainda tenha a lista antiga, exibe a lista antiga para não quebrar o site
        musica_selecionada = st.selectbox(
            "Pesquise pelo Artista ou Nome da Música (Modo de Compatibilidade):",
            options=["-- Selecione uma música --"] + catalogo
        )
        musica_manual = ""
        if musica_selecionada == "-- Selecione uma música --":
            musica_manual = st.text_input("Digitar música manualmente (Artista - Título):")
    else:
        st.warning("⚠️ Não foi possível carregar o catálogo automático. Digita abaixo:")
        musica_manual = st.text_input("Artista - Título da Música:")
        musica_selecionada = "-- Selecione uma música --"

    # Botão de envio obrigatório dentro do bloco 'with st.form'
    botao_enviar = st.form_submit_button("🚀 Enviar Pedido para o DJ")

# 2. Processar o envio do pedido fora do formulário
if botao_enviar:
    if not nome_cliente.strip():
        st.error("❌ Por favor, digita o teu nome ou mesa antes de enviar.")
    else:
        nome_musica_final = ""
        arquivo_hd_real = "Manual"
        
        if musica_selecionada != "-- Selecione uma música --":
            nome_musica_final = musica_selecionada
            # Se for o catálogo novo (dicionário), resgata o arquivo com pontos. Se for lista, envia o próprio nome.
            if isinstance(catalogo, dict):
                arquivo_hd_real = catalogo.get(musica_selecionada, musica_selecionada)
            else:
                arquivo_hd_real = musica_selecionada
        elif musica_manual.strip():
            nome_musica_final = musica_manual.strip()
        
        if not nome_musica_final:
            st.error("❌ Por favor, seleciona uma música ou digita uma manualmente.")
        else:
            # Estrutura do pedido enviada para o Firebase
            dados_pedido = {
                "cantor": nome_cliente.strip(),
                "musica": nome_musica_final,
                "arquivo_real": arquivo_hd_real,
                "timestamp": time.time()
            }
            
            try:
                envio = requests.post(URL_FIREBASE_PEDIDOS, json=dados_pedido, timeout=5)
                if envio.status_code == 200:
                    st.success(f"🎉 Perfeito, {nome_cliente}! O teu pedido de '{nome_musica_final}' foi enviado para a fila.")
                else:
                    st.error("❌ Erro ao enviar para a nuvem. Tenta novamente.")
            except Exception as e:
                st.error(f"❌ Erro de conexão: {e}")
