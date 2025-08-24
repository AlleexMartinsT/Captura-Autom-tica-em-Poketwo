from functions.bibliotecas import *
from paths.path import *
from functions.funcoes_principais import *
from regions.region_ss import *
from functions.config import *
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

interface()

palavras_banidas = carregar_banlist()
pokemon_validos = carregar_pokemons()

if not esta_aberto("chrome.exe"):
   subprocess.Popen([chrome_path,url])
   time.sleep(1)
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
                    while check_fail: # Loop de tentativas até acertar o nome
                        nome = extrair_nome_pokemon()

                        check_fail, tentativa, contador = enviar_comando_discord(nome, check_fail, tentativa, contador)
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