from functions.bibliotecas import *
from paths.path import *
from regions.region_ss import RATE_LIMIT_REGION
from functions.global_var import *


def checar_rate_limit():
    """Verifica se o aviso de flood do Discord apareceu"""
    try:
        pos = pyautogui.locateOnScreen(RATE_LIMIT_IMG, confidence=0.8, region=RATE_LIMIT_REGION)
        screenshot = pyautogui.screenshot(region=RATE_LIMIT_REGION)
        screenshot.save("debug_fail_area.png")
    except pyautogui.ImageNotFoundException:
        pos = None
    return pos is not None