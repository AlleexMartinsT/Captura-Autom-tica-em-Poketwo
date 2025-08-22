import pyautogui
import time

# Defina os valores
center_x, center_y = 660, 550
width, height = 490, 400
# Calcule a região
region = (center_x - width//2, center_y - height//2, width, height)
time.sleep(0.1)
# Exibe as coordenadas da região
print(f"Região: {region}")

# Opcional: Desenhar um retângulo na tela para visualizar a área

screenshot = pyautogui.screenshot(region=region)
screenshot.save("regiao_capturada.png")
print("A região foi salva como 'regiao_capturada.png'.")

# Opcional: Capturar e salvar a região como imagem para verificar
