import time
import requests
import os

# CONFIGURAÇÕES
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedido.json"
PASTA_LOCAL = r"G:\F.F KARAOKE"

def verificar_e_tocar():
    try:
        resp = requests.get(URL_FIREBASE_PEDIDOS, timeout=5)
        if resp.status_code == 200 and resp.json():
            dados = resp.json()
            # Nome vindo da nuvem (ex: "amor.mp4")
            musica_nuvem = dados.get("musica", "").strip()
            
            if musica_nuvem:
                print(f"\n🎵 Pedido recebido: {musica_nuvem}")
                
                # Vamos procurar um ficheiro que contenha o nome pedido
                # Se o pedido for "amor.mp4", ele procura qualquer ficheiro que tenha "amor" no nome
                nome_base = musica_nuvem.replace(".mp4", "").replace(".mp3", "")
                
                ficheiro_encontrado = None
                for arquivo in os.listdir(PASTA_LOCAL):
                    if nome_base.lower() in arquivo.lower():
                        ficheiro_encontrado = os.path.join(PASTA_LOCAL, arquivo)
                        break
                
                if ficheiro_encontrado:
                    print(f"✅ Ficheiro correspondente encontrado: {ficheiro_encontrado}")
                    os.startfile(ficheiro_encontrado)
                else:
                    print(f"❌ ERRO: Não encontrei nenhum ficheiro que contenha '{nome_base}' na pasta.")

                # Apaga o pedido após tentar processar
                requests.delete(URL_FIREBASE_PEDIDOS)
                print("🧹 Pedido processado.")
                
    except Exception as e:
        print(f"Erro na conexão: {e}")

if __name__ == "__main__":
    print(f"Monitor ativo. À espera de pedidos em {PASTA_LOCAL}...")
    while True:
        verificar_e_tocar()
        time.sleep(3)
