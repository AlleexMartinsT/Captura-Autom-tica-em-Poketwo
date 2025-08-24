import sys, os, re, unicodedata, tkinter as tk
from tkinter import messagebox, ttk
from difflib import get_close_matches

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths.path import POKEMON_FILE, BANLIST_FILE


def normalizar_nome(nome: str) -> str:
    """Remove acentos, espaços e pontuações para comparar nomes"""
    nome = nome.lower().strip()
    # Remove acentos
    nome = "".join(
        c for c in unicodedata.normalize("NFD", nome) if unicodedata.category(c) != "Mn"
    )
    # Remove caracteres especiais
    nome = re.sub(r"[\.\-’'´`]", "", nome)
    nome = re.sub(r"\s+", "", nome)  # remove todos os espaços
    return nome


def centralizar_janela(root, largura=500, altura=400):
    root.update_idletasks()
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    x = (largura_tela // 2) - (largura // 2)
    y = (altura_tela // 2) - (altura // 2)
    root.geometry(f"{largura}x{altura}+{x}+{y}")


# Carrega lista de pokémons válidos
with open(POKEMON_FILE, "r", encoding="utf-8") as f:
    pokemon_validos = [linha.strip() for linha in f if linha.strip()]

pokemon_normalizados = {normalizar_nome(p): p for p in pokemon_validos}

# Carrega banlist
with open(BANLIST_FILE, "r", encoding="utf-8") as f:
    banidos = [linha.strip() for linha in f if linha.strip()]

banidos_resultados = []
for nome in banidos:
    norm = normalizar_nome(nome)
    if norm in pokemon_normalizados:
        banidos_resultados.append((nome, pokemon_normalizados[norm]))
    else:
        similares = get_close_matches(norm, pokemon_normalizados.keys(), n=1, cutoff=0.85)
        if similares and similares[0] in pokemon_normalizados:
            banidos_resultados.append((nome, pokemon_normalizados[similares[0]]))
        # Se não existe → ignora totalmente


def salvar_remocoes():
    novos_banidos = banidos[:]
    for i, (errado, _) in enumerate(banidos_resultados):
        if var_list[i].get() == 1:  # marcado para remover
            novos_banidos.remove(errado)

    with open(BANLIST_FILE, "w", encoding="utf-8") as f:
        for b in novos_banidos:
            f.write(b + "\n")

    messagebox.showinfo("Sucesso", "Banlist atualizada!")
    root.destroy()


if banidos_resultados:
    root = tk.Tk()
    root.title("Gerenciar Banlist")

    centralizar_janela(root, largura=550, altura=450)
    ttk.Label(root, text="Pokémon encontrados na lista:", font=("Arial", 12, "bold")).pack(pady=10)

    frame = ttk.Frame(root)
    frame.pack(padx=10, pady=10, fill="both", expand=True)

    var_list = []
    for errado, correto in banidos_resultados:
        var = tk.IntVar()
        texto = f"{errado} → {correto}"
        chk = ttk.Checkbutton(frame, text=texto, variable=var)
        chk.pack(anchor="w")
        var_list.append(var)

    ttk.Button(root, text="Salvar Alterações", command=salvar_remocoes).pack(pady=10)

    root.mainloop()
else:
    print("✅ Nenhum Pokémon válido encontrado na banlist.")
