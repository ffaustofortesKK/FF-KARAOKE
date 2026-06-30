import streamlit as st
import requests
import json
from mega import Mega  # Certifique-se de ter 'mega-py' nos requirements.txt

# --- CONFIGURAÇÕES ---
URL_FIREBASE = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"
LINK_PASTA_MEGA = "https://mega.nz/fm/FyETjZzS"

st.set_page_config(page_title="FF Karaoke Cloud", page_icon="🎤", layout="centered")
st.title("🎤 FF KARAOKE CLOUD")

# --- FUNÇÃO PARA PEGAR AS MÚSICAS EM TEMPO REAL DO MEGA ---
@st.cache_data(ttl=600)  # Atualiza a cada 10 minutos para não bloquear o site
def carregar_catalogo_do_mega():
    try:
        mega = Mega()
        # Login anónimo seguro para ler link público
        m_anonimo = mega.login()
        # Busca os ficheiros diretamente da URL da pasta
        arquivos = m_anonimo.get_files_from_url(LINK_PASTA_MEGA)
        
        lista_nomes = []
        if arquivos:
            for file_id, file_info in arquivos.items():
                nome = file_info.get('a', {}).get('n', '')
                if nome:
                    lista_nomes.append(nome)
        return lista_nomes
    except Exception as e:
        # Se falhar a ligação com o MEGA por limite de tráfego, retorna vazio
        return []

# Carrega a lista direto da nuvem
catalogo_musicas = carregar_catalogo_do_mega()

# --- INTERFACE ---
cantor = st.text_input("1º Nome do Cantor (Seu Nome):", placeholder="Ex: Fausto Fortes")
busca_musica = st.text_input("2º Pesquisar Música (Digite o nome da música ou artista):", placeholder="Ex: Paulo Flores").strip()

musica_final = ""
modo_manual = False

if busca_musica:
    if catalogo_musicas:
        resultados = [m for m in catalogo_musicas if busca_musica.lower() in m.lower()]
        
        if resultados:
            st.markdown("⬇️ **Músicas encontradas na sua nuvem MEGA:**")
            musica_final = st.selectbox("Escolha a versão exata:", resultados, key="selecao_resultado")
        else:
            st.error("❌ Essa música não está disponível no nosso acervo da nuvem MEGA.")
            modo_manual = True
            pedido_manual = st.text_input("📝 Pedido Manual (Introduza o nome para o DJ verificar):", value=busca_musica)
            musica_final = pedido_manual
    else:
        # Se o MEGA demorar a responder, o sistema entra em modo de segurança (Manual)
        modo_manual = True
        musica_final = busca_musica

st.write("---")
btn_enviar = st.button("3º Enviar Pedido 🚀", use_container_width=True)

if btn_enviar:
    if not cantor:
        st.error("⚠️ Por favor, digite o seu nome no 1º campo.")
    elif not busca_musica:
        st.error("⚠️ Por favor, pesquise uma música no 2º campo.")
    else:
        dados = {"cantor": cantor.strip(), "musica": musica_final.strip()}
        try:
            resposta = requests.post(URL_FIREBASE, data=json.dumps(dados), timeout=5)
            if resposta.status_code == 200:
                if modo_manual:
                    st.warning("⚠️ Seu pedido foi enviado, mas não temos a certeza que ela esteja disponível em Karaoke.")
                else:
                    st.success(f"🎉 Pedido de **{dados['musica']}** enviado com sucesso!")
                    st.balloons()
        except Exception as e:
            st.error(f"Erro: {e}")
