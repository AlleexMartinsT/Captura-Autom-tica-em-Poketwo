from functions.bibliotecas import *
from paths.path import *
from regions.region_ss import POKEMON_REGION, POKEMON_REGION_UP, WRONG_POKE
from functions.config import *
from functions.funcoes_aux import *
from functions import config

def esperar_pokemon():  
    delay_envio = 0.2
    print("🔄 Iniciando envio de mensagens para spawnar Pokémon...")
    contador = 1
    while True:
        time.sleep(0.4)  # pequena pausa para evitar uso excessivo da CPU
        if discord_crash():
            print("O Discord estava fechado ou com crash. Abrindo o Discord...")
            pos = pyautogui.locateOnScreen(DISCORD_BUTTON, confidence=0.8)
            pyautogui.moveTo(pos)
            pyautogui.click()
            time.sleep(3)
            print("Discord aberto com sucesso!")
        if contador > 60:
            print("⚠️ Contador excedeu 60. Reiniciando...")
            contador = -1
            return contador
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
            alt_tab("Chrome")
            time.sleep(config.SLEEP_ALT_TAB) # Permitir usuario alterar o time.sleep no futuro. (Padrão: 0.2)
            return contador
        else:
            contador += 1

def clicar_icone_busca():
    """Localiza e clica no ícone de busca por imagem"""
    tentativas = 0
    while True:
        tentativas += 1
        try:
            pos = pyautogui.locateCenterOnScreen(ICONE_PATH, confidence=0.8)
        except pyautogui.ImageNotFoundException:
            pos = None

        if pos:
            pyautogui.moveTo(pos)
            pyautogui.click()
            print(f"🖱️ Ícone de busca clicado!")
            return True
        else:
            print(f"❌ Ícone não encontrado. Tentando novamente... ({tentativas})")
            # Clique fora da tela para tentar atualizar a interface
            pyautogui.click(1572, 383)
            pyautogui.press('esc')
            time.sleep(1)  # pequena pausa antes de tentar de novo

def carregar_imagem_pokemon(caminho_imagem):
    """Cola o caminho do arquivo e confirma a busca"""
    time.sleep(1)
    pyautogui.press("enter")
    print(f"tempo usado: {config.SLEEP_CTRLV}")
    time.sleep(config.SLEEP_CTRLV)
    pyperclip.copy(caminho_imagem)
    pyautogui.hotkey("ctrl", "v")  # Cola o caminho
    time.sleep(0.5)
    pyautogui.press("enter")
    print("📸 Imagem do Pokémon carregada para pesquisa!")

def extrair_nome_pokemon():
    palavras_banidas = carregar_banlist()
    """Captura o nome mais repetido no resultado do Google Lens e registra no log"""
    screenshot = pyautogui.screenshot()
    img_bgr = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Extrai texto da tela
    texto = pytesseract.image_to_string(img_bgr, lang="por+eng")
    texto = texto.replace("\n", " ").replace("\r", " ")
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
    elif nome_pokemon == "flabébé": # Problemas com Flabébé / Flabebe.
        nome_pokemon = "flabebe"

    return nome_pokemon

def enviar_comando_discord(nome_pokemon,check_fail,tentativa, contador):
    """Volta ao Discord e digita o comando"""
    comando_restante = f"catch {nome_pokemon}"
    
    if not nome_pokemon:
        return
    if tentativa > 3:
        print("Não encontrou nenhuma das imagens")
        pyautogui.typewrite(".clear 8")
        pyautogui.press("enter")
        check_fail = 2
        return check_fail,tentativa
        
    alt_tab("Discord")  # volta para o Discord
    pyautogui.press("enter")
    time.sleep(0.5)
    
    # Seleciona tudo e apaga
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')  # ou 'delete'
    time.sleep(0.5)
    pyautogui.typewrite("@Poketwo")
    pyautogui.press("tab")
    time.sleep(0.5)
    pyautogui.typewrite(comando_restante)
    pyautogui.press("enter")
    print(f"💬 Comando enviado: @Poketwo{comando_restante}")
    time.sleep(3) # Permitir usuario alterar o time.sleep no futuro. (Padrão: 3)

    check_fail = 0 

    pos = pyautogui.locateOnScreen(POKEMON_FAIL, confidence=0.8, region=WRONG_POKE)
    # Se falhar em capturar um pokemon
    print("Tentativa:", tentativa)
    if pos:
        print("Encontrou a imagem do FAIL")
        contador += 2
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
        print("adicionando palavra banida")
        adicionar_banida(nome_pokemon)
        tentativa += 1
        print("tentativa +1")
        check_fail = 1
        print("check_fail=1")
    else:
        pos = pyautogui.locateOnScreen(POKEMON_CAPTURED, confidence=0.6, region=WRONG_POKE)
        achievement = pyautogui.locateOnScreen(ACHIEVEMENT, confidence=0.8, region=WRONG_POKE)
        if pos:
            print("Encontrou a imagem CAPTURED")
            check_fail = 0
            if achievement:
                print("Conqusita alcançada")
                check_fail = 0
        else:    
            print("Nada encontrado")
            pyautogui.typewrite(f".clear {contador}")
            pyautogui.press("enter")
            check_fail = 2
    return check_fail,tentativa,contador

def interface():
    root = tk.Tk()
    root.title("Configuração de Time Sleep")

    largura_janela = 300
    altura_janela = 200
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura_janela // 2)
    pos_y = (altura_tela // 2) - (altura_janela // 2)
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

    opcoes = ["0.5", "1.0", "1.5", "2.0"]
    altTab_capturaPokemonDiscord = ["0.2", "0.5", "1.0"]
    
    tk.Label(root, text="Tempo para abrir Discord:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    combo_discord = ttk.Combobox(root, values=opcoes, state="readonly")
    combo_discord.set(str(config.SLEEP_DISCORD))
    combo_discord.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(root, text="Tempo para Lens carregar:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    combo_lens = ttk.Combobox(root, values=opcoes, state="readonly")
    combo_lens.set(str(config.SLEEP_LENS))
    combo_lens.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(root, text="Tempo para o Ctrl+V no google").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    combo_retry = ttk.Combobox(root, values=opcoes, state="readonly")
    combo_retry.set(str(config.SLEEP_CTRLV))
    combo_retry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(root, text="Tempo ALT+TAB:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
    combo_alt_tab = ttk.Combobox(root, values=altTab_capturaPokemonDiscord, state="readonly")
    combo_alt_tab.set(str(config.SLEEP_ALT_TAB))
    combo_alt_tab.grid(row=3, column=1, padx=5, pady=5)
    
    def salvar_config():
        try:
            config.SLEEP_DISCORD = float(combo_discord.get())
            config.SLEEP_LENS = float(combo_lens.get())
            config.SLEEP_CTRLV = float(combo_retry.get())
            config.SLEEP_ALT_TAB = float(combo_alt_tab.get())
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
            root.destroy()
        except ValueError:
            messagebox.showerror("Erro", "Selecione apenas valores válidos.")

    tk.Button(root, text="Salvar", command=salvar_config).grid(row=4, columnspan=2, pady=10)
    
    return root.mainloop()

    