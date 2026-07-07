import streamlit as st

# CSS para criar o efeito de "Placa" da imagem
st.markdown("""
    <style>
    .container-registo {
        background-color: #1a1a1a;
        border: 2px solid #b8860b;
        border-radius: 15px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 0 20px rgba(184, 134, 11, 0.5);
        max-width: 600px;
        margin: auto;
    }
    .titulo-registo { color: #d4af37; font-size: 32px; font-weight: bold; margin-bottom: 20px; }
    .social-link { color: #d4af37; font-size: 18px; text-decoration: none; display: block; margin: 10px 0; }
    </style>
""", unsafe_allow_html=True)

# Função da tela de Registo
def render_registo():
    st.markdown('<div class="container-registo">', unsafe_allow_html=True)
    st.markdown('<p class="titulo-registo">Registo Inicial</p>', unsafe_allow_html=True)
    
    st.markdown('<a class="social-link" href="https://www.instagram.com/ff_karaoke">📸 INSTAGRAM: @ff_karaoke</a>', unsafe_allow_html=True)
    st.markdown('<a class="social-link" href="https://www.tiktok.com/@ff.karaoke">🎵 TIK TOK: @ff.karaoke</a>', unsafe_allow_html=True)
    
    nome = st.text_input("Nome", placeholder="Digite seu nome aqui...")
    
    st.markdown('<p style="color:white; margin-top:20px;">Confirmo que segui o Grupo FF no Instagram e no TikTok</p>', unsafe_allow_html=True)
    check_social = st.checkbox("Li e aceito")
    
    # O botão aqui ficará abaixo dos campos
    if st.button("Concluir Registo", use_container_width=True):
        if nome and check_social:
            st.session_state.nome = nome
            st.session_state.registado = True
            st.rerun()
        else:
            st.error("Por favor, preencha o nome e aceite os termos.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Lógica principal
if 'registado' not in st.session_state:
    st.session_state.registado = False

if not st.session_state.registado:
    render_registo()
else:
    st.write("Bem-vindo à tela de pedidos!")
