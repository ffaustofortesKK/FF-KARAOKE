else:
    # DEFINA AS COLUNAS ANTES DE USAR 'with col_main'
    col_main, col_cam = st.columns([2, 1])
    
    with col_main:
        st.markdown(f'<p style="color:#FFD700; font-weight:bold; font-size:24px;">Bem-vindo, {st.session_state.nome}!</p>', unsafe_allow_html=True)
        
        # --- BUSCA E PEDIDO ---
        busca = st.text_input("Título / Cantor:", key="input_busca")
        
        if st.button("Pesquisar"):
            try:
                resp = requests.get(URL_FIREBASE_CATALOGO, timeout=5)
                dados = resp.json()
                cat = list(dados.keys()) if isinstance(dados, dict) else dados
                st.session_state.resultados = [m for m in cat if busca.lower() in m.lower()]
                st.rerun()
            except: 
                pass

        if 'resultados' in st.session_state and st.session_state.resultados:
            escolha = st.selectbox("Selecione a música:", st.session_state.resultados, key="select_musica")
            
            if st.button("Confirmar Pedido"):
                requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": escolha})
                st.markdown('<div class="success-box">O seu pedido foi enviado com sucesso!</div>', unsafe_allow_html=True)
                st.balloons()
                
                # LIMPEZA
                st.session_state.resultados = None
                st.session_state.input_busca = "" 
                st.rerun() 
        
        # --- PEDIDO MANUAL ---
        st.markdown("<br><label>Título/Cantor que não estão na lista:</label>", unsafe_allow_html=True)
        manual = st.text_input("Digite aqui manualmente:", key="input_manual")
        
        if st.button("Enviar Pedido Manual"):
            if manual:
                requests.post(URL_FIREBASE_PEDIDOS, json={"cantor": st.session_state.nome, "musica": manual})
                st.markdown('<div class="warning-box">O seu pedido foi enviado!</div>', unsafe_allow_html=True)
                st.session_state.input_manual = ""
                st.rerun()
