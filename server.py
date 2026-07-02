import time
import requests
import json
import os
from mega import Mega

# --- CONFIGURAÇÕES ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedido.json"
URL_FIREBASE_CATALOGO = "https://grupoffkaraoke-default-rtdb.firebaseio.com/catalogo.json"
PASTA_MUSICAS_LOCAL = r"G:\F.F KARAOKE"
LINK_PASTA_MEGA = "https://mega.nz/folder/xxxxxx#yyyyyy" 

def atualizar_catalogo_no_firebase():
    print("\n🔄 [MEGA] A ler a pasta de Karaoke na nuvem...")
    try:
        mega = Mega()
        m_anonimo = mega.login() 
        arquivos = m_anonimo.get_files_from_url(LINK_PASTA_MEGA)
        
        lista_musicas = []
        if arquivos:
            for file_id, file_info in arquivos.items():
                nome = file_info.get('a', {}).get('n', '')
                if nome and not nome.startswith('.'):
                    lista_musicas.append(nome)
            
            lista_musicas.sort()
            requests.put(URL_FIREBASE_CATALOGO, json=lista_musicas)
            print(f"✅ [SUCESSO] {len(lista_musicas)} músicas atualizadas no Firebase!")
    except Exception as e:
        print(f"❌ Erro ao ler o MEGA: {e}")

def tocar_musica_local(musica_pedido):
    """Procura o ficheiro na pasta local e abre-o."""
    print(f"🔍 Procurando por: {musica_pedido} na pasta {PASTA_MUSICAS_LOCAL}")
    
    # Lista todos os ficheiros da pasta G:\
    for ficheiro in os.listdir(PASTA_MUSICAS_LOCAL):
        # Compara apenas o nome (ignorando maiúsculas e minúsculas)
        if musica_pedido.lower() in ficheiro.lower():
            caminho_completo = os.path.join(PASTA_MUSICAS_LOCAL, ficheiro)
            print(f"▶️ A abrir: {caminho_completo}")
            try:
                os.startfile(caminho_completo) # Abre com o player padrão do Windows
                return True
            except Exception as e:
                print(f"Erro ao abrir ficheiro: {e}")
    return False

if __name__ == "__main__":
    print("🎤 FF KARAOKE CLOUD — Monitor Iniciado")
    atualizar_catalogo_no_firebase()
    
    print("\n🎧 [ESCUTA ATIVA] Aguardando pedidos...")
    
    while True:
        try:
            # 1. Busca pedido
            resposta = requests.get(URL_FIREBASE_PEDIDOS, timeout=5)
            if resposta.status_code == 200 and resposta.json():
                pedidos = resposta.json()
                
                # Se o Firebase for uma lista ou dicionário, processamos
                # Aqui assumimos que estás a apagar o pedido após ler
                pedido = pedidos # Se for um único pedido
                
                cantor = pedido.get("cantor", "Desconhecido")
                musica = pedido.get("musica", "")
                
                if musica:
                    print(f"\n🚀 [NOVO PEDIDO] Cantor: {cantor} | Música: {musica}")
                    
                    # 2. Tenta tocar
                    achou = tocar_musica_local(musica)
                    
                    if achou:
                        print("✅ Música encontrada e enviada para o leitor!")
                    else:
                        print("⚠️ Música não encontrada na pasta G:\\. Verifique o nome!")
                    
                    # 3. Limpa o pedido do Firebase para não repetir
                    requests.delete(URL_FIREBASE_PEDIDOS)
                    print("🧹 Pedido removido da nuvem.")
        
        except Exception as e:
            print(f"Erro de conexão: {e}")
            
        time.sleep(3)
