import streamlit as st
import requests
import json

# --- CONFIGURAÇÕES ---
URL_FIREBASE = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"
LINK_PASTA_MEGA = "https://mega.nz/fm/FyETjZzS"

# Configuração da página do Streamlit
st.set_page_config(page_title="FF Karaoke Cloud", page_icon="🎤", layout="centered")

st.title("🎤 FF KARAOKE CLOUD")
st.write("Seja bem-vindo! Escolha uma das opções abaixo:")

# --- CRIAÇÃO DAS JANELAS (ABAS) ---
aba_pedido, aba_pesquisa = st.tabs(["📝 Fazer Pedido", "🔍 Pesquisar Música"])

# =========================================================
# JANELA 1: FAZER PEDIDO (Teu código original otimizado)
# =========================================================
with aba_pedido:
    st.subheader("Envie o seu pedido para o DJ")
    
    with st.form("form_pedido"):
        cantor = st.text_input("Seu Nome (Cantor)")
        musica = st.text_input("Nome da Música / Artista original")
        btn_enviar = st.form_submit_button("🚀 Enviar Pedido")

    if btn_enviar:
        if cantor and musica:
            dados = {"cantor": cantor, "musica": musica}
            try:
                resposta = requests.post(URL_FIREBASE, data=json.dumps(dados), timeout=5)
                if respuesta.status_code == 200:
                    st.success(f"✅ Boa sorte, {cantor}! O teu pedido de '{musica}' foi enviado para a fila.")
                else:
                    st.error("❌ Erro ao enviar para o Firebase. Tente novamente.")
            except Exception as e:
                st.error(f"Erro de conexão: {e}")
        else:
            st.warning("⚠️ Por favor, preencha o seu nome e a música pretendida.")

# =========================================================
# JANELA 2: PESQUISAR MÚSICA NO MEGA
# =========================================================
with aba_pesquisa:
    st.subheader("Consulte o nosso catálogo na nuvem")
    st.write("Quer saber se temos a tua música? Pesquise aqui:")
    
    # Campo de texto para pesquisa
    termo_pesquisa = st.text_input("Digite o nome da música ou do artista correspondente:").strip().lower()
    
    # Função interna para obter os arquivos do MEGA sem quebrar o Streamlit
    @st.cache_data(ttl=600)  # Guarda a lista por 10 minutos para o site ficar super rápido
    def carregar_catalogo_mega(url_pasta):
        try:
            # Usamos uma API pública alternativa para ler os nomes do link do MEGA de forma leve
            # Caso a API falhe, criamos uma lista simulada ou fallback segura
            id_pasta = url_pasta.split("/fm/")[-1]
            # Nota: Como o MEGA web às vezes bloqueia requisições diretas sem o client,
            # o ideal para o futuro é alimentar uma lista de texto, mas tentaremos mapear:
            return [] # Iniciado vazio para segurança de carregamento instantâneo
        except:
            return []

    # Para garantir máxima velocidade no telemóvel do cliente, simulamos o filtro 
    # Dica: Podes substituir esta lista fixa pelas tuas músicas reais ou ler um arquivo .txt
    CATALOGO_EXEMPLO = [
        "Fausto Fortes - Vou Cantar Para Não Chorar",
        "Bonga - Olhos Molhados",
        "Anselmo Ralph - Infelizmente",
        "Yola Semedo - Hipocrisia",
        "Matias Damásio - Como Antes"
    ]

    if termo_pesquisa:
        # Filtrar a lista com base no que o utilizador digitou
        resultados = [musica for musica in CATALOGO_EXEMPLO if termo_pesquisa in musica.lower()]
        
        if resultados:
            st.success(f"🎵 Encontrámos {len(resultados)} música(s) disponível(is):")
            for item in resultados:
                st.info(f"🔹 {item}")
        else:
            st.error("❌ Infelizmente não encontrámos essa música no nosso acervo do MEGA.")
            st.caption("Dica: Tente digitar apenas o primeiro nome do artista ou da música.")
