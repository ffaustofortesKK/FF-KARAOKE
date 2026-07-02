import time
import requests
import os
import subprocess
import shutil

# --- CONFIGURAÇÕES ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedido.json"
PASTA_MUSICAS_LOCAL = r"G:\F.F KARAOKE"
PASTA_TEMP = r"C:\KaraokeTemp"

# Garante que a pasta temporária existe
if not os.path.exists(PASTA_TEMP):
    os.makedirs(PASTA_TEMP)

def tocar_musica_local(musica_pedido):
    """Copia a música para um nome simples e abre-a."""
    print(f"\n🔍 À procura de: {musica_pedido}")
    
    for arquivo in os.listdir(PASTA_MUSICAS_LOCAL):
        if musica_pedido.lower().strip() in arquivo.lower().strip():
            caminho_origem = os.path.join(PASTA_MUSICAS_LOCAL, arquivo)
            caminho_destino = os.path.join(PASTA_TEMP, "temp_karaoke.mp4")
            
            print(f"▶️ Ficheiro encontrado: {arquivo}")
            
            try:
                # Copia o ficheiro original para um nome "limpo"
                shutil.copy2(caminho_origem, caminho_destino)
                
                # Abre o ficheiro limpo usando o comando 'start' do Windows
                cmd = f'start "" "{caminho_destino}"'
                subprocess.Popen(cmd, shell=True)
                
                print("✅ Ficheiro copiado e enviado para o player com sucesso.")
                return True
            except Exception as e:
                print(f"❌ Erro ao copiar ou abrir: {e}")
                return False
    
    print("❌ Música não encontrada na pasta local.")
    return False

if __name__ == "__main__":
    print(f"🎤 MONITOR FF KARAOKE ATIVO")
    print(f"Origem: {PASTA_MUSICAS_LOCAL}")
    print(f"Destino Temp: {PASTA_TEMP}")
    print("----------------------------")
    
    while True:
        try:
            # Busca pedido na nuvem
            resp = requests.get(URL_FIREBASE_PEDIDOS, timeout=5)
            if resp.status_code == 200 and resp.json():
                dados = resp.json()
                musica = dados.get("musica", "").strip()
                
                if musica:
                    print(f"\n🚀 Novo Pedido: {musica}")
                    sucesso = tocar_musica_local(musica)
                    
                    # Limpa o pedido da nuvem após o processamento
                    requests.delete(URL_FIREBASE_PEDIDOS)
                    print("🧹 Pedido removido da nuvem.")
        
        except Exception as e:
            print(f"Erro de conexão: {e}")
            
        time.sleep(3)
