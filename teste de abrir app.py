import subprocess
import psutil
import pygetwindow as gw

# Caminho do executável do Chrome
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
url = "https://www.google.com/search?q=a&rlz=1C1FKPE_enBR1112BR1113&oq=a&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIGCAEQRRg8MgYIAhBFGDwyBggDEEUYPDIGCAQQBRhAMgYIBRAFGEAyBggGEAUYQDIGCAcQBRhA0gEIMTQ2MmowajeoAgCwAgA&sourceid=chrome&ie=UTF-8"

# Abre o Chrome)

def esta_aberto(processo_nome):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == processo_nome:
            return True
    return False

# Exemplo para Chrome no Windows
if not esta_aberto("chrome.exe"):
    subprocess.Popen([chrome_path,url])
else:
    print("O Chrome já está aberto!")


# Procura todas as janelas do Chrome
janelas = gw.getWindowsWithTitle("Google Chrome")
if janelas:
    janelas[0].activate()  # traz a primeira janela para frente
