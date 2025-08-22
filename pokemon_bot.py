from functions.bibliotecas import *
from paths.path import *
from functions.funcoes_principais import esperar_pokemon
from regions.region_ss import *
from functions.global_var import *
from functions.funcoes_aux import *

# Garante que 'locateOnScreen' NÃO levante exceção quando não achar
try:
    pyautogui.useImageNotFoundException(False)
except Exception:
    pass

# ====== CONFIGURAÇÕES ======

# Caminho do Tesseract (se precisar no Windows)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Templates e imagens
if template is None:
    print(f"ERRO: Não foi possível carregar o template '{TEMPLATE_PATH}'")
    exit()

# ====== FUNÇÕES ======

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
    center_x, center_y = 679, 935
    width, height = 747, 156

    # Calcula a região (top-left x, top-left y, largura, altgitura)
    WRONG_POKE = (center_x - width//2, center_y - height//2, width, height)

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

palavras_banidas = carregar_banlist()
pokemon_validos = carregar_pokemons()

if not esta_aberto("chrome.exe"):
   subprocess.Popen([chrome_path,url])
else:
    print("O Chrome já está aberto!")

adicionar_cabecalho(BANLIST_FILE)
adicionar_cabecalho(LOG_FILE)

alt_tab()
        
print("Pressione qualquer tecla para continuar...")
keyboard.read_event()
 
while True:
    contador = esperar_pokemon()
    if contador == -1:
        alt_tab()
    else:
        print("Procurando a tela do Google...")
        tentativas = 0
        check_fail = 1
        tentativa = 0
        while True:
            tentativas += 1
            if is_google_screen():
                if clicar_icone_busca():
                    carregar_imagem_pokemon(POKEMON_IMG_PATH)
                    time.sleep(2.5)  # espera o Lens carregar o resultado
                    # Loop de tentativas até acertar o nome
                    while check_fail:
                        nome = extrair_nome_pokemon()

                        check_fail, tentativa = enviar_comando_discord(nome, check_fail, tentativa)
                        if check_fail == 2:
                            break
                        if check_fail:
                            print("❌ Nome incorreto. Tentando novamente no Google Lens...")
                            pyautogui.hotkey("alt", "tab")  # volta para o Chrome
                            time.sleep(0.5)
                            clicar_icone_busca()
                            carregar_imagem_pokemon(POKEMON_IMG_PATH)
                            time.sleep(2)
                        else:
                            print("✅ Pokémon capturado com sucesso!")
                            log_path = LOG_FILE
                            try:
                                with open(log_path, "a", encoding="utf-8") as f:  # 'a' cria se não existir
                                    f.write(f"{nome}\n")
                                print(f"📝 Nome registrado em {log_path}")
                            except Exception as e:
                                print(f"❌ Erro ao registrar no log: {e}")
                            print("Iniciando time sleep de 0.5")
                            time.sleep(0.5)
                            print("Concluido")
                            print("Iniciando contador de clear")
                            clear_mensagem(contador)
                            print("Contador de clear concluido")
                            break
                break
            else:
                print(f"❌ Não é a tela do Google. Tentando novamente... ({tentativas})")
                pyautogui.hotkey('alt', 'tab')
                time.sleep(0.2)