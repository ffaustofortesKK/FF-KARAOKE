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
    """Calcula a posição exata e atualizada do cliente com base na fila real."""
    try:
        resp = requests.get(URL_FIREBASE_PEDIDOS, timeout=5)
        dados = resp.json()
        if not dados:
            return False, 0, 0
        
        lista_pedidos = []
        if isinstance(dados, dict):
            for pedido_id, info in dados.items():
                if isinstance(info, dict):
                    info_com_id = info.copy()
                    info_com_id["firebase_id"] = pedido_id
                    lista_pedidos.append(info_com_id)
        elif isinstance(dados, list):
            for idx_l, i in enumerate(dados):
                if isinstance(i, dict):
                    info_com_id = i.copy()
                    info_com_id["firebase_id"] = str(idx_l)
                    lista_pedidos.append(info_com_id)

        posicao = 0
        encontrou = False
        for idx, info in enumerate(lista_pedidos):
            # Compara o nome do cantor ignorando maiúsculas/minúsculas e espaços
            if info.get("cantor", "").strip().lower() == nome_cantor.strip().lower():
                encontrou = True
                posicao = idx + 1
                break
                
        return encontrou, posicao, len(lista_pedidos)
    except:
        return False, 0, 0

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
        font-size: 3.92rem;
        text-align: center;
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.9);
        animation: oscilarTexto 1.2s ease-in-out infinite;
    }}

    .aviso-fila {{
        color: #FFD700;
        font-weight: bold;
        font-size: 24px;
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

    .marquee-topo {{
        width: 100%;
        overflow: hidden;
        white-space: nowrap;
        box-sizing: border-box;
        margin-bottom: 15px;
    }}

    .marquee-topo span {{
        display: inline-block;
        padding-left: 100%;
        animation: marquee 15s linear infinite;
        color: #00ffcc;
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
    st.markdown("""
        <div class="marquee-topo">
            <span>À medida que as músicas anteriores forem tocadas e finalizadas, a sua posição atualizará automaticamente.</span>
        </div>
    """, unsafe_allow_html=True)

    nome_usuario = st.session_state.nome
    nome_com_emoji = f"🎙️ {nome_usuario} 🎶"

    st.markdown(f"""
        <div>
            <h2>Bem-vindo,</h2>
            <div class="nome-comico">{nome_com_emoji}</div>
        </div>
    """, unsafe_allow_html=True)

    tem_pedido_ativo, posicao_fila, total_fila = obter_dados_fila(st.session_state.nome)

    if tem_pedido_ativo:
        if posicao_fila == 1:
            texto_posicao = "Você é a seguir!!!"
        else:
            texto_posicao = f"{posicao_fila}º Lugar"

        st.markdown(f"""
            <div class="container-mic">
                <div class="posicao-sobre-mic">{texto_posicao}</div>
                <div class="icone-mic">🎤</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="aviso-fila">
                ⚠️ O seu pedido está ativo na fila de reprodução (Total na fila: {total_fila}).
            </div>
        """, unsafe_allow_html=True)
        
        # Botão para iniciar a música do cliente se houver mais de 3 músicas na fila
        if total_fila > 3:
            st.markdown("---")
            st.info("🔥 A fila tem mais de 3 músicas! Se desejar disparar o seu turno diretamente, pode usar o botão abaixo:")
            if st.button("▶️ Iniciar a Minha Música (Cliente)", use_container_width=True):
                try:
                    resp = requests.get(URL_FIREBASE_PEDIDOS, timeout=5)
                    dados = resp.json()
                    if isinstance(dados, dict):
                        for pid, pinfo in dados.items():
                            if isinstance(pinfo, dict) and pinfo.get("cantor", "").strip().lower() == st.session_state.nome.strip().lower():
                                requests.delete(f"https://grupoffkaraoke-default-rtdb.firebaseio.com/pedidos/{pid}.json")
                                break
                except:
                    pass
                
                st.success("Comando enviado! A sua música foi acionada.")
                st.balloons()
                time.sleep(2)
                st.rerun()

        time.sleep(4)
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

        if st.button("Não achou pesquisa aqui!!!"):
            st.session_state.mostrar_manual = not st.session_state.mostrar_manual
            st.rerun()

        if st.session_state.mostrar_manual:
            st.subheader("PEDIDOS FORA DA LISTA DE MÚSICAS")
            pedido_manual = st.text_input("Digite o nome da música:")

            if st.button("Confirmar Pedido Manual"):
                if pedido_manual and pedido_manual.strip():
                    requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": pedido_manual.strip(), "status": "manual"})
                    st.balloons()
                    st.success("O seu pedido foi enviado com sucesso!")
                    st.session_state.mostrar_manual = False
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("Por favor, digite o nome da música.")

    st.divider()
    if st.button("Sair"):
        st.session_state.registado = False
        st.session_state.mostrar_manual = False
        st.rerun()
