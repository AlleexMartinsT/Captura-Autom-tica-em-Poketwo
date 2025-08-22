from functions.bibliotecas import *
from paths.path import *
from regions.region_ss import POKEMON_REGION, POKEMON_REGION_UP, WRONG_POKE
from functions.funcoes_aux import checar_rate_limit
from functions.global_var import *
from functions.funcoes_aux import *

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

def extrair_nome_pokemon():
    """Captura o nome mais repetido no resultado do Google Lens e registra no log"""
    time.sleep(3)
    screenshot = pyautogui.screenshot()
    img_bgr = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Extrai texto da tela
    texto = pytesseract.image_to_string(img_bgr, lang="por+eng")
    texto = texto.replace("\n", " ").replace("\r", " ")

    # Conta palavras
    palavras = {}
    for palavra in texto.split():
        palavra_limpa = palavra.strip(".,!?:;()[]\"'").lower()
        if (palavra_limpa 
            and len(palavra_limpa) >= 4  # mínimo de 4 letras
            and palavra_limpa not in palavras_banidas):
            palavras[palavra_limpa] = palavras.get(palavra_limpa, 0) + 1

    if not palavras:
        print("❌ Nenhuma palavra válida encontrada!")
        return None

    # Pega a palavra mais repetida
    nome_pokemon = max(palavras, key=palavras.get)
    print(f"📋 Nome detectado: {nome_pokemon}")
    
    if nome_pokemon == "mime": # Problemas com Mr.Mime / Mr Mime.
        nome_pokemon = "mr mime"

    return nome_pokemon

def carregar_imagem_pokemon(caminho_imagem):
    """Cola o caminho do arquivo e confirma a busca"""
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    pyperclip.copy(caminho_imagem)
    pyautogui.hotkey("ctrl", "v")  # Cola o caminho
    time.sleep(1)
    pyautogui.press("enter")
    print("📸 Imagem do Pokémon carregada para pesquisa!")
    time.sleep(3)

    """Captura o nome mais repetido no resultado do Google Lens e registra no log"""
    screenshot = pyautogui.screenshot()
    img_bgr = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Extrai texto da tela
    texto = pytesseract.image_to_string(img_bgr, lang="por+eng")
    texto = texto.replace("\n", " ").replace("\r", " ")

     # Aguarda carregar e clica fora da área para limpar a tela
    pyautogui.click(1572, 383)
    pyautogui.press('esc')
    print("🖱️ Clique fora da imagem para preparar próxima captura!")
    # Conta palavras
    palavras = {}   
    for palavra in texto.split():
        palavra_limpa = palavra.strip(".,!?:;()[]\"'").lower()
        if (palavra_limpa 
            and len(palavra_limpa) >= 4  # mínimo de 4 letras
            and palavra_limpa not in palavras_banidas):
            palavras[palavra_limpa] = palavras.get(palavra_limpa, 0) + 1

    if not palavras:
        print("❌ Nenhuma palavra válida encontrada!")
        return None

    # Pega a palavra mais repetida
    nome_pokemon = max(palavras, key=palavras.get)
    print(f"📋 Nome detectado: {nome_pokemon}")
    
    if nome_pokemon == "mime": # Problemas com Mr.Mime / Mr Mime.
        nome_pokemon = "mr mime"

    return nome_pokemon

def enviar_comando_discord(nome_pokemon,check_fail,tentativa):
    """Volta ao Discord e digita o comando"""
    if not nome_pokemon:
        return
    if tentativa > 3:
        print("Não encontrou nenhuma das imagens")
        pyautogui.typewrite(".clear 8")
        pyautogui.press("enter")
        check_fail = 2
        return check_fail,tentativa
        
    pyautogui.hotkey("alt", "tab")  # volta para o Discord
    pyautogui.press("enter")
    time.sleep(0.5)
    
    # Seleciona tudo e apaga
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')  # ou 'delete'
    time.sleep(0.5)
    pyautogui.typewrite("@Poketwo")
    pyautogui.press("tab")
    time.sleep(0.5)

    # Digita o comando de captura
    comando_restante = f"catch {nome_pokemon}"
    pyautogui.typewrite(comando_restante)
    pyautogui.press("enter")
    print(f"💬 Comando enviado: @Poketwo{comando_restante}")
    time.sleep(3)

    check_fail = 0 

    pos = pyautogui.locateOnScreen(POKEMON_FAIL, confidence=0.8, region=WRONG_POKE)
    # Se falhar em capturar um pokemon
    print("Tentativa:", tentativa)
    if pos:
        print("Encontrou a imagem do FAIL")
        #screenshot = pyautogui.screenshot(region=WRONG_POKE)
        #screenshot.save("debug_fail_area.png")
        if tentativa > 0:
            print(f"Tentativa {tentativa} falha no (primeiro if), tentando novamente...")
            print("usando pokemon_region_up")
            screenshot = pyautogui.screenshot(region=POKEMON_REGION_UP)
            screenshot.save(POKEMON_IMG_PATH)
        else:
            print("usando pokemon_region")
            screenshot = pyautogui.screenshot(region=POKEMON_REGION)
            screenshot.save(POKEMON_IMG_PATH)
        adicionar_banida(nome_pokemon)
        tentativa += 1
        check_fail = 1
    else:
        pos = pyautogui.locateOnScreen(POKEMON_CAPTURED, confidence=0.6, region=WRONG_POKE)
        achievement = pyautogui.locateOnScreen(ACHIEVEMENT, confidence=0.8, region=WRONG_POKE)
        if pos:
            print("Encontrou a imagem CAPTURED")
            check_fail = 0
            if achievement:
                print("Conqusita alcançada")
                check_fail = 0    

    return check_fail,tentativa
