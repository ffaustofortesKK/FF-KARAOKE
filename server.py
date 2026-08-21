import streamlit as st
import requests
import time 
import yt_dlp

# --- CONFIGURAÇÕES ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos.json"
URL_FIREBASE_FILA_ATUAL = "https://grupoffkaraoke-default-rtdb.firebaseio.com/fila_atual.json"
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

def pesquisar_youtube(termo):
    ydl_opts = {
        'format': 'bestaudio',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{termo}", download=False)
            if 'entries' in info and len(info['entries']) > 0:
                entry = info['entries'][0]
                return entry.get('webpage_url'), entry.get('title')
    except:
        pass
    return None, None

def verificar_estado_pedido(nome_cantor):
    """
    Verifica se o cliente já tem pedido na fila atual do PC ou na nuvem.
    Retorna: (estado, posicao, total_fila)
    Estados: 'na_fila_atual', 'na_nuvem', 'nao_encontrado'
    """
    try:
        # 1. Verificar se já passou para a Fila de Reprodução Atual do PC
        resp_atual = requests.get(URL_FIREBASE_FILA_ATUAL, timeout=5)
        dados_atual = resp_atual.json()
        
        if dados_atual:
            lista_atual = []
            if isinstance(dados_atual, dict):
                for pid, info in dados_atual.items():
                    if isinstance(info, dict):
                        lista_atual.append(info)
            elif isinstance(dados_atual, list):
                lista_atual = [i for i in dados_atual if isinstance(i, dict)]
                
            for idx, info in enumerate(lista_atual):
                if info.get("cantor", "").strip().lower() == nome_cantor.strip().lower():
                    return "na_fila_atual", idx + 1, len(lista_atual)

        # 2. Verificar se ainda está na nuvem (aguardando operador passar)
        resp_cloud = requests.get(URL_FIREBASE_PEDIDOS, timeout=5)
        dados_cloud = resp_cloud.json()
        
        if dados_cloud:
            lista_cloud = []
            if isinstance(dados_cloud, dict):
                for pid, info in dados_cloud.items():
                    if isinstance(info, dict):
                        lista_cloud.append(info)
            elif isinstance(dados_cloud, list):
                lista_cloud = [i for i in dados_cloud if isinstance(i, dict)]
                
            for info in lista_cloud:
                if info.get("cantor", "").strip().lower() == nome_cantor.strip().lower():
                    return "na_nuvem", 0, len(lista_cloud)
        
        return "nao_encontrado", 0, 0
    except:
        return "nao_encontrado", 0, 0

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

    @keyframes comicoMover {{
        0% {{ transform: translateY(0px) rotate(0deg); }}
        25% {{ transform: translateY(-8px) rotate(-3deg); }}
        50% {{ transform: translateY(0px) rotate(0deg); }}
        75% {{ transform: translateY(-8px) rotate(3deg); }}
        100% {{ transform: translateY(0px) rotate(0deg); }}
    }}

    @keyframes oscilarTexto {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.08); }}
        100% {{ transform: scale(1); }}
    }}

    .container-mic {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 20px;
        margin-bottom: 20px;
        position: relative;
    }}

    .icone-mic {{
        font-size: 216px; 
        animation: girarRelogio 4s linear infinite;
        text-shadow: 0px 0px 25px rgba(255, 215, 0, 0.8);
        display: inline-block;
    }}

    .posicao-sobre-mic {{
        position: absolute;
        top: 35%;
        z-index: 10;
        color: #FFD700;
        font-weight: bold;
        font-size: 2.8rem;
        text-align: center;
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.9);
        animation: oscilarTexto 1.2s ease-in-out infinite;
    }}

    .aviso-fila {{
        color: #FFD700;
        font-weight: bold;
        font-size: 22px;
        text-align: center;
        margin-top: 5px;
        margin-bottom: 10px;
    }}

    .nome-comico {{
        font-size: 4.5rem; 
        font-weight: bold;
        color: #28a745;
        display: inline-block;
        animation: comicoMover 1.5s ease-in-out infinite;
        text-shadow: 0px 2px 0px rgba(40, 167, 69, 0.4), 
                     0px 4px 0px rgba(40, 167, 69, 0.2), 
                     0px 12px 15px rgba(0, 0, 0, 0.9);
        margin-bottom: 10px;
    }}

    .marquee-rodape {{
        width: 100%;
        overflow: hidden;
        white-space: nowrap;
        box-sizing: border-box;
        margin-top: 20px;
        background: rgba(0, 0, 0, 0.6);
        padding: 10px 0;
        border-radius: 5px;
    }}

    .marquee-rodape span {{
        display: inline-block;
        padding-left: 100%;
        animation: marquee 12s linear infinite;
        color: #00ffcc;
        font-size: 18px;
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
if 'mostrar_manual' not in st.session_state: st.session_state.mostrar_manual = False

if not st.session_state.registado:
    st.subheader("📝 Registo Inicial")
    nome = st.text_input("Nome:")
    if st.button("Concluir Registo"):
        if nome:
            st.session_state.nome = nome
            st.session_state.registado = True
            st.session_state.mostrar_manual = False
            st.rerun()
else:
    nome_usuario = st.session_state.nome
    nome_com_emoji = f"🎙️ {nome_usuario} 🎶"

    st.markdown(f"""
        <div>
            <h2>Bem-vindo,</h2>
            <div class="nome-comico">{nome_com_emoji}</div>
        </div>
    """, unsafe_allow_html=True)

    # Verifica se já tem pedido em andamento (nuvem ou fila atual)
    estado_pedido, posicao_fila, total_fila = verificar_estado_pedido(st.session_state.nome)

    if estado_pedido == "na_nuvem":
        # Enquanto estiver na nuvem aguardando o operador
        st.markdown(f"""
            <div class="container-mic">
                <div class="posicao-sobre-mic">Actualizando a<br>Sua posição</div>
                <div class="icone-mic">🎤</div>
            </div>
        """, unsafe_allow_html=True)

        # Rodapé com polinhas a passar
        st.markdown("""
            <div class="marquee-rodape">
                <span>• • • • • • • • • • • • • • • • • • • • • • • • • • • • • •</span>
            </div>
        """, unsafe_allow_html=True)

        time.sleep(4)
        st.rerun()

    elif estado_pedido == "na_fila_atual":
        # Quando passar para a fila de reprodução atual do PC
        texto_posicao = "Você é a seguir!!!" if posicao_fila == 1 else f"{posicao_fila}º Lugar"

        st.markdown(f"""
            <div class="container-mic">
                <div class="posicao-sobre-mic">{texto_posicao}</div>
                <div class="icone-mic">🎤</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="aviso-fila">
                ✅ O seu pedido já está ativo na Fila de Reprodução Atual!
            </div>
        """, unsafe_allow_html=True)
        
        if total_fila > 3:
            if st.button("▶️ Iniciar a Minha Música (Cliente)", use_container_width=True):
                st.success("Comando enviado!")
                st.balloons()
                time.sleep(2)
                st.rerun()

        time.sleep(4)
        st.rerun()

    else:
        # Se NÃO tem pedido ativo, mostra os campos de pesquisa normalmente para pedir nova música
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

        if st.button("Não achou clica aqui!!"):
            st.session_state.mostrar_manual = not st.session_state.mostrar_manual
            st.rerun()

        if st.session_state.mostrar_manual:
            st.subheader("🎵 PEDIDOS FORA DA LISTA DE MÚSICAS")
            pedido_manual = st.text_input("Digite o nome da música que pretende cantar:")

            if st.button("Enviar Pedido Manual"):
                if pedido_manual and pedido_manual.strip():
                    with st.spinner("A pesquisar link correspondente no YouTube..."):
                        url_yt, titulo_yt = pesquisar_youtube(pedido_manual.strip())
                    
                    link_final = url_yt if url_yt else "Link não encontrado automaticamente"
                    nome_musica_final = f"{pedido_manual.strip()} (YT: {link_final})"

                    requests.post(URL_FIREBASE_PEDIDOS, json={
                        "cantor": st.session_state.nome, 
                        "musica": nome_musica_final, 
                        "status": "manual"
                    })
                    
                    st.balloons()
                    st.warning("SEU PEDIDO FOI ENVIADO, MAIS NEM TODAS AS MUSICAS EXISTEM EM KARAOKE")
                    st.session_state.mostrar_manual = False
                    time.sleep(4)
                    st.rerun()
                else:
                    st.error("Por favor, digite o nome da música.")

    st.divider()
    if st.button("Sair"):
        st.session_state.registado = False
        st.session_state.mostrar_manual = False
        st.rerun()
