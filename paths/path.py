from functions.bibliotecas import *


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # sobe uma pasta

TEMPLATE_PATH = os.path.join(BASE_DIR,"images", "google_logo_template.png")
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