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

    @keyframes girarRelogio {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}

    .container-mic {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 40px;
        margin-bottom: 20px;
    }}

    .icone-mic {{
        font-size: 216px; /* Aumentado 20% do anterior (180px * 1.2) */
        animation: girarRelogio 4s linear infinite;
        text-shadow: 0px 0px 25px rgba(255, 215, 0, 0.8);
        display: inline-block;
    }}

    .aviso-fila {{
        color: #FFD700;
        font-weight: bold;
        font-size: 22px;
        text-align: center;
        margin-top: 15px;
        margin-bottom: 10px;
    }}

    .numero-posicao {{
        color: #FFFFFF;
        font-weight: bold;
        font-size: 28px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.9);
    }}

    /* Nome: Aumentado 40% adicional (em relação ao anterior), verde, com efeito reflexo */
    .nome-reflexo {{
        font-size: 4.5rem; 
        font-weight: bold;
        color: #28a745;
        text-shadow: 0px 2px 0px rgba(40, 167, 69, 0.4), 
                     0px 4px 0px rgba(40, 167, 69, 0.2), 
                     0px 12px 15px rgba(0, 0, 0, 0.9);
        margin-bottom: 20px;
    }}

    .marquee-rodape {{
        width: 100%;
        overflow: hidden;
        white-space: nowrap;
        box-sizing: border-box;
        margin-top: 30px;
        margin-bottom: 20px;
    }}

    .marquee-rodape span {{
        display: inline-block;
        padding-left: 100%;
        animation: marquee 15s linear infinite;
        color: #FFFFFF;
        font-size: 16px;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.9);
    }}

    @keyframes marquee {{
        0%   {{ transform: translate(0, 0); }}
        100% {{ transform: translate(-100%, 0); }}
    }}

    .stButton > button {{
        background-color: #007BFF !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        border: none !important;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.8) !important;
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
    st.markdown(f"""
        <div>
            <h2>Bem-vindo,</h2>
            <div class="nome-reflexo">{st.session_state.nome}!</div>
        </div>
    """, unsafe_allow_html=True)

    tem_pedido_ativo, posicao_fila = obter_dados_fila(st.session_state.nome)

    if tem_pedido_ativo:
        st.markdown("""
            <div class="container-mic">
                <div class="icone-mic">🎤</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="aviso-fila">
                ⚠️ Você já tem uma música na fila! A sua posição atual é: <span class="numero-posicao">{posicao_fila}º</span> lugar.
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class="marquee-rodape">
                <span>À medida que as músicas anteriores forem tocadas e finalizadas, a sua posição atualizará automaticamente.</span>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Atualizar Minha Posição"):
            st.rerun()
    else:
        busca = st.text_input("🔍 Pesquisar Música no catálogo:")
        escolha = None
        if busca:
            cat = obter_catalogo()
            resultados = [m for m in cat if busca.lower() in str(m).lower()]
            if resultados:
                escolha = st.selectbox("Selecione:", resultados)

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

        st.subheader("PEDIDOS FORA DA LISTA DE MÚSICAS")
        pedido_manual = st.text_input("Digite o nome da música:")

        if st.button("Confirmar Pedido Manual"):
            if pedido_manual and pedido_manual.strip():
                requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": pedido_manual.strip(), "status": "manual"})
                st.balloons()
                st.success("O seu pedido foi enviado com sucesso!")
                time.sleep(2)
                st.rerun()
            else:
                st.error("Por favor, digite o nome da música.")

    st.divider()
    if st.button("Sair"):
        st.session_state.registado = False
        st.rerun()
