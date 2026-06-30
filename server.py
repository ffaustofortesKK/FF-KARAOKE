import streamlit as st
import requests
import json

# --- CONFIGURAÇÕES DO FIREBASE ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedido.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"

st.title("🎤 FF KARAOKE CLOUD")
st.subheader("Faz o teu pedido de música em tempo real!")

# 1. Procurar o catálogo atualizado no Firebase
@st.cache_data(ttl=60)  # Atualiza a lista a cada 60 segundos
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
    
    if catalogo:
        # Pega nos nomes limpos (chaves do dicionário) para o cliente pesquisar
        opcoes_musicas = list(catalogo.keys())
        
        # Cria a barra de pesquisa inteligente com os nomes limpos (Ex: "Anselmo Meu Amor")
        musica_selecionada = st.selectbox(
            "Pesquise pelo Artista ou Nome da Música:",
            options=["-- Selecione uma música --"] + opcoes_musicas
        )
        
        # Opção alternativa se não encontrar
        musica_manual = ""
        if musica_selecionada == "-- Selecione uma música --":
            st.info("💡 Não encontras a tua música? Podes digitar o nome manualmente abaixo:")
            musica_manual = st.text_input("Digitar música manualmente (Artista - Título):")
    else:
        st.warning("⚠️ Não foi possível carregar o catálogo automático. Digita abaixo:")
        musica_manual = st.text_input("Artista - Título da Música:")
        musica_selecionada = "-- Selecione uma música --"

    # Botão de envio
    botao_enviar = st.form_submit_button("🚀 Enviar Pedido para o DJ")

# 2. Processar o envio do pedido quando o botão for clicado
if botao_enviar:
    if not nome_cliente.strip():
        st.error("❌ Por favor, digita o teu nome ou mesa antes de enviar.")
    else:
        # Define qual o texto e o arquivo real que vão para o DJ
        nome_musica_final = ""
        arquivo_hd_real = "Manual"
        
        if musica_selecionada != "-- Selecione uma música --":
            nome_musica_final = musica_selecionada
            # Resgata o nome com pontos original (Ex: "Anselmo.Meu amor.mp4") para o teu HD dar Play
            arquivo_hd_real = catalogo[musica_selecionada]
        elif musica_manual.strip():
            nome_musica_final = musica_manual.strip()
        
        if not nome_musica_final:
            st.error("❌ Por favor, seleciona uma música ou digita uma manualmente.")
        else:
            # Cria o pacote de dados estruturado para o Firebase
            dados_pedido = {
                "cantor": nome_cliente.strip(),
                "musica": nome_musica_final,
                "arquivo_real": arquivo_hd_real,
                "timestamp": time.time() if 'time' in globals() else None
            }
            
            # Envia para o nó de pedidos do Firebase
            try:
                envio = requests.post(URL_FIREBASE_PEDIDOS, json=dados_pedido, timeout=5)
                if envio.status_code == 200:
                    st.success(f"🎉 Perfeito, {nome_cliente}! O teu pedido de '{nome_musica_final}' foi enviado. Aguarda a tua vez!")
                else:
                    st.error("❌ Erro ao enviar para a nuvem. Tenta novamente.")
            except Exception as e:
                st.error(f"❌ Erro de conexão: {e}")
