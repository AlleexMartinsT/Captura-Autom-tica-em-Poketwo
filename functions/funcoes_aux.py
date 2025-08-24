from functions.bibliotecas import *
from paths.path import *
from regions.region_ss import RATE_LIMIT_REGION
from functions.config import *
from functions.funcoes_principais import *

def checar_rate_limit():
    """Verifica se o aviso de flood do Discord apareceu"""
    try:
        pos = pyautogui.locateOnScreen(RATE_LIMIT_IMG, confidence=0.8, region=RATE_LIMIT_REGION)
        screenshot = pyautogui.screenshot(region=RATE_LIMIT_REGION)
        screenshot.save("debug_fail_area.png")
    except pyautogui.ImageNotFoundException:
        pos = None
    return pos is not None

def check_orb_match(screenshot_gray, template_gray, min_matches=20):
    """Verifica similaridade usando ORB"""
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(template_gray, None)
    kp2, des2 = orb.detectAndCompute(screenshot_gray, None)

    if des1 is None or des2 is None:
        return False

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    return len(matches) >= min_matches

def check_ocr_text(screenshot, keywords):
    """Verifica se algum texto esperado está na tela"""
    text = pytesseract.image_to_string(screenshot, lang="por+eng")
    text = text.lower()
    return any(keyword.lower() in text for keyword in keywords)

def carregar_lista(arquivo):
    if not os.path.exists(arquivo):
        return []
    with open(arquivo, "r", encoding="utf-8") as f:
        # strip() remove espaços e quebras de linha
        # o if linha.strip() garante que só entra linha com conteúdo
        return [linha.strip() for linha in f.readlines() if linha.strip()]

def adicionar_cabecalho(arquivo):
    agora = datetime.now()
    data_str = agora.strftime("%d/%m/%Y")
    hora_str = agora.strftime("%H:%M")

    cabecalho = f"-------------{data_str} {hora_str}-----------"
    
    linhas = carregar_lista(arquivo)

    if cabecalho not in linhas:
        # Abre em modo append binário só para checar o último caractere
        with open(arquivo, "rb") as f:
            f.seek(0, 2)  # vai para o fim do arquivo
            vazio = f.tell() == 0  # se o arquivo está vazio
            if not vazio:
                f.seek(-1, 2)
                ultimo_char = f.read(1)
            else:
                ultimo_char = b"\n"

        with open(arquivo, "a", encoding="utf-8") as f:
            # se o último char não for quebra de linha, adiciona uma antes
            if ultimo_char not in (b"\n", b"\r"):
                f.write("\n")
            f.write(cabecalho + "\n")

    print(f"Cabeçalho adicionado ao arquivo {arquivo}")

def clear_mensagem(contador):
    pyautogui.typewrite(f".clear {contador+3}") 
    pyautogui.press("enter")
    time.sleep(1.5)
  
# ====== MANIPULAÇÃO DE TELA ======

def alt_tab():
    for sufixo in ["Chrome", " - Discord"]:
        janelas = [w for w in gw.getAllWindows() if w.title.endswith(sufixo)]
        if janelas:
            focar_janela(janelas[0])
    
def esta_aberto(processo_nome):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == processo_nome:
            return True
    return False

def focar_janela(janela):
    app = Application().connect(handle=janela._hWnd)
    app.window(handle=janela._hWnd).set_focus()

def is_google_screen():
    """Combina ORB + OCR para confirmar se é a tela do Google"""
    screenshot = pyautogui.screenshot()
    img_bgr = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    orb_result = check_orb_match(img_gray, template)
    ocr_result = check_ocr_text(img_bgr, ["Google", "Pesquisa Google"])

    print(f"ORB: {orb_result} | OCR: {ocr_result}")
    return orb_result or ocr_result

def discord_crash():
    """Verifica se o Discord travou"""
    try:
        pos = pyautogui.locateOnScreen(DISCORD_CRASH, confidence=0.8)
        screenshot = pyautogui.screenshot()
        screenshot.save(BASE_DIR + "/images/debug_discord_crash.png")
    except pyautogui.ImageNotFoundException:
        pos = None
    return pos is not None

# ====== MANIPULAÇÃO DA BAN_LIST ======

def salvar_banlist(lista):
    with open(BANLIST_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lista))

def adicionar_banida(palavra, palavras_banidas):
    palavras_banidas = carregar_banlist()
    pokemon_validos = carregar_pokemons()
    """Adiciona uma nova palavra na banlist.txt se ainda não estiver lá"""
    if palavra not in pokemon_validos:
        if palavra not in palavras_banidas:
            palavras_banidas.append(palavra)
            salvar_banlist(palavras_banidas)
            print(f"[BANLIST] '{palavra}' adicionado à lista de palavras ignoradas!")
    else:
        print("Esta palavra é um pokemon!")

def carregar_banlist():
    if not os.path.exists(BANLIST_FILE):
        return []
    with open(BANLIST_FILE, "r", encoding="utf-8") as f:
        return [linha.strip() for linha in f.readlines()]
    
# ====== MANIPULAÇÃO DA POKEMON_LIST ======

def carregar_pokemons():
    """Carrega todos os pokémons válidos a partir do arquivo pokemon_list.txt"""
    arquivo = POKEMON_FILE
    if not os.path.exists(arquivo):
        raise FileNotFoundError(f"Arquivo {arquivo} não encontrado!")

    with open(arquivo, "r", encoding="utf-8") as f:
        return [
            linha.strip().lower()
            for linha in f.readlines()
            if linha.strip()  # ignora linhas em branco
        ] 