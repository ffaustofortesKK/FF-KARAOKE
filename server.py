import streamlit as st
import requests
import time 

# --- CONFIGURAÇÕES ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"
LINK_LOGO = "https://cdn.phototourl.com/free/2026-07-03-793a0f18-6143-44c8-b56e-e44af828c30c.png"
URL_SOM_PALMAS = "https://www.soundjay.com/misc/sounds/applause-2.mp3"

st.set_page_config(page_title="FF KARAOKE CLOUD", layout="wide")

@st.cache_data(ttl=300)
def obter_catalogo():
    try:
        resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
        dados = resp.json()
        if isinstance(dados, list):
            return dados
        if isinstance(dados, dict):
            return list(dados.values())
        return []
    except:
        return []

def obter_dados_fila(nome_cantor):
    """Verifica se o cantor tem pedido ativo e calcula a sua posição exata na fila."""
    try:
        resp = requests.get(URL_FIREBASE_PEDIDOS, timeout=5)
        dados = resp.json()
        if not dados:
            return False, 0
        
        lista_pedidos = []
        if isinstance(dados, dict):
            for pedido_id, info in dados.items():
                if isinstance(info, dict):
                    lista_pedidos.append(info)
        elif isinstance(dados, list):
            lista_pedidos = [i for i in dados if isinstance(i, dict)]

        # Encontrar a posição (índice + 1) do utilizador na lista de pedidos
        posicao = 0
        encontrou = False
        for idx, info in enumerate(lista_pedidos):
            if info.get("cantor", "").strip().lower() == nome_cantor.strip().lower():
                encontrou = True
                posicao = idx + 1
                break
                
        return encontrou, posicao
    except:
        return False, 0

st.markdown(f"""
    <style>
    .stApp {{ 
        background: linear-gradient(rgba(9, 10, 15, 0.85), rgba(9, 10, 15, 0.85)), url('{LINK_LOGO}');
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        color: white; 
    }}

    /* Estilo e Animação do Microfone a Girar */
    @keyframes girarMicrofone {{
        0% {{ transform: rotate(0deg); }}
        25% {{ transform: rotate(10deg); }}
        75% {{ transform: rotate(-10deg); }}
        100% {{ transform: rotate(0deg); }}
    }}

    .container-mic {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 30px;
        margin-bottom: 30px;
    }}

    .icone-mic {{
        font-size: 100px;
        animation: girarMicrofone 3s infinite ease-in-out;
        text-shadow: 0px 0px 20px rgba(255, 215, 0, 0.6);
    }}
    </style>
""", unsafe_allow_html=True)

if 'registado' not in st.session_state: st.session_state.registado = False

if not st.session_state.registado:
    st.subheader("📝 Registo Inicial")
    nome = st.text_input("Nome:")
    if st.button("Concluir Registo"):
        if nome:
            st.session_state.nome = nome
            st.session_state.registado = True
            st.rerun()
else:
    st.title(f"Bem-vindo, {st.session_state.nome}!")

    # Verificar se o utilizador está na fila e qual a posição
    tem_pedido_ativo, posicao_fila = obter_dados_fila(st.session_state.nome)

    if tem_pedido_ativo:
        # Exibir o microfone gigante a girar no centro
        st.markdown("""
            <div class="container-mic">
                <div class="icone-mic">🎤</div>
            </div>
        """, unsafe_allow_html=True)

        st.warning(f"⚠️ Você já tem uma música na fila! A sua posição atual é: **{posicao_fila}º** lugar.")
        st.info("À medida que as músicas anteriores forem tocadas e finalizadas, a sua posição atualizará automaticamente.")
        
        # Botão para atualizar a página e verificar a nova posição
        if st.button("🔄 Atualizar Minha Posição"):
            st.rerun()
    else:
        # --- 1. PESQUISA NO CATÁLOGO ---
        busca = st.text_input("🔍 Pesquisar Música no catálogo:")

        escolha = None
        if busca:
            cat = obter_catalogo()
            resultados = [m for m in cat if busca.lower() in str(m).lower()]
            
            if resultados:
                escolha = st.selectbox("Selecione:", resultados)

        # --- ENVIO CATALOGO ---
        if escolha:
            st.write(f"Música selecionada: **{escolha}**")
            if st.button("Confirmar Pedido"):
                requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": str(escolha).strip()})
                st.balloons()
                st.success("O seu pedido foi enviado com sucesso!")
                st.audio(URL_SOM_PALMAS, autoplay=True)
                time.sleep(2)
                st.rerun()

        st.divider()

        # --- 2. CAMPO PEDIDO MANUAL ---
        st.subheader("Manual")
        pedido_manual = st.text_input("Não achou? Digite o nome da música:")

        if st.button("Confirmar Pedido Manual"):
            if pedido_manual and pedido_manual.strip():
                payload = {
                    "cantor": st.session_state.nome, 
                    "musica": pedido_manual.strip(), 
                    "status": "manual"
                }
                requests.post(URL_FIREBASE_PEDIDOS, json=payload)
                st.balloons()
                st.success("O seu pedido foi enviado com sucesso!")
                st.warning("Nota: O seu pedido foi enviado, mas nem todas as músicas existem em Karaoke.")
                time.sleep(3)
                st.rerun()
            else:
                st.error("Por favor, digite o nome da música.")

    st.divider()
    if st.button("Sair"):
        st.session_state.registado = False
        st.rerun()
