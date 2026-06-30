import time
import requests
import json
from mega import Mega

# --- CONFIGURAÇÕES DO FIREBASE ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedido.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"

# --- CONFIGURAÇÕES DO MEGA ---
# IMPORTANTE: Use o link público que contém a palavra 'folder' ou 'file'
# Não use o link que tem 'fm', pois o Python não consegue ler o 'File Manager' privado.
LINK_PASTA_MEGA = "https://mega.nz/folder/xxxxxx#yyyyyy" 

def atualizar_catalogo_no_firebase():
    print("\n🔄 [MEGA] A ler a pasta de Karaoke na nuvem...")
    try:
        mega = Mega()
        m_anonimo = mega.login() # Login anónimo seguro
        arquivos = m_anonimo.get_files_from_url(LINK_PASTA_MEGA)
        
        lista_musicas = []
        if arquivos:
            for file_id, file_info in arquivos.items():
                nome_ficheiro = file_info.get('a', {}).get('n', '')
                # Filtra apenas arquivos válidos (ignora pastas ou arquivos ocultos do sistema)
                if nome_ficheiro and not nome_ficheiro.startswith('.'):
                    lista_musicas.append(nome_ficheiro)
        
        if lista_musicas:
            # Organiza por ordem alfabética para facilitar a busca do cliente
            lista_musicas.sort()
            # Envia a lista completa para o nó /catalogo do Firebase
            requests.put(URL_FIREBASE_CATALOGO, data=json.dumps(lista_musicas))
            print(f"✅ [SUCESSO] {len(lista_musicas)} músicas da nuvem enviadas para o Firebase!")
        else:
            print("⚠️ A pasta do MEGA parece estar vazia ou o link está incorreto.")
            
    except Exception as e:
        print(f"❌ Erro ao ler o MEGA: {e}")
        print("Certifique-se de que o link da pasta é público (formato 'folder').")

def buscar_e_limpar_pedido():
    try:
        resposta = requests.get(URL_FIREBASE_PEDIDOS, timeout=5)
        if resposta.status_code == 200:
            dados = resposta.json()
            if not dados:
                return None
            requests.delete(URL_FIREBASE_PEDIDOS)
            return dados
    except Exception as e:
        print(f"Erro na comunicação com a nuvem: {e}")
    return None

if __name__ == "__main__":
    print("🎤 FF KARAOKE CLOUD — Sistema Iniciado")
    print("-----------------------------------------")
    
    # 1. Atualiza o catálogo no Firebase assim que o programa abre
    atualizar_catalogo_no_firebase()
    
    print("\n🎧 [ESCUTA AKTIVADA] Aguardando novos pedidos do site...")
    print("---")
    
    # 2. Mantém o loop original escutando os pedidos dos clientes
    while True:
        pedido = buscar_e_limpar_pedido()
        if pedido:
            cantor = pedido.get("cantor", "").strip()
            musica = pedido.get("musica", "").strip()
            
            if cantor and musica:
                print("\n🚀 [NOVO PEDIDO RECEBIDO!]")
                print(f"🎤 Cantor/Grupo: {cantor}")
                print(f"🎵 Música: {musica}")
                print("✅ Removido da fila para evitar duplicados.")
                print("-----------------------------------------")
        
        time.sleep(3)
