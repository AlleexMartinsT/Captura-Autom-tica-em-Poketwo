from functions.bibliotecas import *
from paths.path import *
from regions.region_ss import POKEMON_REGION
from functions.funcoes_aux import checar_rate_limit
from functions.global_var import *

def esperar_pokemon():
    delay_envio = 0.2
    print("🔄 Iniciando envio de mensagens para spawnar Pokémon...")
    contador = 1
    while True:
        if contador > 60:
            print("⚠️ Contador excedeu 60. Reiniciando...")
            contador = -1
            return contador
        time.sleep(0.5)
        if checar_rate_limit():
            delay_envio += 0.5
            print(f"⚠️ Rate limit detectado! Novo delay: {delay_envio:.1f}s")
            time.sleep(5.0)
        pyautogui.typewrite(str(contador))
        pyautogui.press("enter")
        time.sleep(delay_envio)  # tempo entre mensagens
        
        pos = pyautogui.locateOnScreen(POKEMON_TRIGGER_FLED, confidence=0.6)

        if pos:
            print("Pokemon fugiu, continuando...")
        else:
            try:
                pos = pyautogui.locateOnScreen(POKEMON_TRIGGER_IMG, confidence=0.8)
            except pyautogui.ImageNotFoundException:
                pos = None

        if pos:
            time.sleep(0.1)
            """Captura a área do Pokémon no Discord e salva"""
            screenshot = pyautogui.screenshot(region=POKEMON_REGION)
            screenshot.save(POKEMON_IMG_PATH)
            pyautogui.hotkey("alt", "tab")
            time.sleep(0.1)
            return contador
        else:
            contador += 1