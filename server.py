import time
import requests
import pyautogui # Instale com: pip install pyautogui
import pygetwindow as gw # Instale com: pip install pygetwindow

# --- CONFIGURAÇÕES ---
URL_FIREBASE_PEDIDOS = "https://grupoffkaraoke-default-rtdb.firebaseio.com/pedido.json"
# Escreva exatamente o nome que aparece no topo da janela do seu programa de Karaoke
NOME_JANELA_KARAOKE = "NomeDoSeuProgramaDeKaraoke" 

def enviar_para_karaoke(nome_musica):
    try:
        # Tenta encontrar a janela do programa de karaoke
        janela = gw.getWindowsWithTitle(NOME_JANELA_KARAOKE)[0]
        janela.activate() # Traz o programa para a frente
        time.sleep(1)
        
        # Escreve o nome da música e pressiona Enter
        pyautogui.write(nome_musica)
        pyautogui.press('enter')
        print(f"✅ Nome da música digitado no programa: {nome_musica}")
        return True
    except Exception as e:
        print(f"❌ Erro ao controlar o programa: {e}")
        return False

# --- LOOP PRINCIPAL ---
while True:
    try:
        resp = requests.get(URL_FIREBASE_PEDIDOS, timeout=5)
        if resp.status_code == 200 and resp.json():
            dados = resp.json()
            musica = dados.get("musica", "").strip()
            
            if musica:
                # Remove a extensão para não atrapalhar a busca
                nome_limpo = musica.replace(".mp4", "").replace(".mp3", "")
                enviar_para_karaoke(nome_limpo)
                
                requests.delete(URL_FIREBASE_PEDIDOS)
    except:
        pass
    time.sleep(3)
