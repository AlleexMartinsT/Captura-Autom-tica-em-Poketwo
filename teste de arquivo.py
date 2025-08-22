import os

def carregar_pokemons():
    """Carrega todos os pokémons válidos a partir do arquivo pokemon_list.txt"""
    arquivo = "pokemon_list.txt"
    if not os.path.exists(arquivo):
        raise FileNotFoundError(f"Arquivo {arquivo} não encontrado!")

    with open(arquivo, "r", encoding="utf-8") as f:
        return [
            linha.strip().lower()
            for linha in f.readlines()
            if linha.strip()  # ignora linhas em branco
        ]

def procurar_pokemon(nome_pokemon):
    """Procura um Pokémon no arquivo"""
    pokemons = carregar_pokemons()
    return nome_pokemon.lower() in pokemons


# 🔹 Exemplo de uso:
while True:
    entrada = input("Digite o nome de um Pokémon (ou 'sair' para encerrar): ").strip()
    if entrada.lower() == "sair":
        break

    if procurar_pokemon(entrada):
        print(f"✅ '{entrada}' está na lista de Pokémons!")
    else:
        print(f"❌ '{entrada}' NÃO foi encontrado.")
