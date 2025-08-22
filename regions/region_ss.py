from functions.bibliotecas import *

# Região onde o Pokémon aparece no Discord
center_x, center_y = 660, 750
width, height = 490, 400
POKEMON_REGION = (center_x - width//2, center_y - height//2, width, height)

# Região onde a mensagem do discord aparece
center_x, center_y = 925, 540
width, height = 485, 170
RATE_LIMIT_REGION = (center_x - width//2, center_y - height//2, width, height)

# Região onde o Pokémon aparece no Discord após duas tentativas falhas
center_x, center_y = 660, 550
width, height = 490, 400
POKEMON_REGION_UP = (center_x - width//2, center_y - height//2, width, height)

# Calcula a região (top-left x, top-left y, largura, altgitura)
center_x, center_y = 679, 935
width, height = 747, 156

WRONG_POKE = (center_x - width//2, center_y - height//2, width, height)