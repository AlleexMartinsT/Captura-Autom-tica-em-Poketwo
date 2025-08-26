from functions.bibliotecas import *


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # sobe uma pasta

TEMPLATE_PATH = os.path.join(BASE_DIR,"images", "google_logo_template.png")
template = cv2.imread(TEMPLATE_PATH, cv2.IMREAD_GRAYSCALE)
ICONE_PATH = os.path.join(BASE_DIR,"images", "icone_busca.png")
POKEMON_IMG_PATH = os.path.join(BASE_DIR,"images", "pokemon_screenshot.png")
POKEMON_TRIGGER_IMG = os.path.join(BASE_DIR,"images", "wild_pokemon.png")
POKEMON_TRIGGER_FLED = os.path.join(BASE_DIR,"images", "wild_pokemon2.png")
POKEMON_CAPTURED = os.path.join(BASE_DIR,"images","congratulations.png")
POKEMON_FAIL = os.path.join(BASE_DIR,"images", "failure.png")
RATE_LIMIT_IMG = os.path.join(BASE_DIR,"images", "rate_limit.png") 
ACHIEVEMENT = os.path.join(BASE_DIR,"images", "conquista.png")  
POKEMON_FILE = os.path.join(BASE_DIR,"archives", "pokemon_list.txt")
LOG_FILE = os.path.join(BASE_DIR,"archives", "log.txt")
BANLIST_FILE = os.path.join(BASE_DIR, "archives", "banlist.txt")
DISCORD_CRASH = os.path.join(BASE_DIR, "images", "discord_crash.png")
DISCORD_BUTTON = os.path.join(BASE_DIR, "images", "discord_button.png")

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
discord_path = r"C:\ProgramData\alex\Discord\Update.exe --processStart Discord.exe"
url = "https://www.google.com/search?q=a&rlz=1C1FKPE_enBR1112BR1113&oq=a&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIGCAEQRRg8MgYIAhBFGDwyBggDEEUYPDIGCAQQBRhAMgYIBRAFGEAyBggGEAUYQDIGCAcQBRhA0gEIMTQ2MmowajeoAgCwAgA&sourceid=chrome&ie=UTF-8"