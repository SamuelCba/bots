#!/usr/bin/env python3
"""
Chrome Multi-Viewer para Kick
Abre 10 ventanas normales y 10 incógnito en Chrome, todas viendo el mismo stream
"""

import time
import threading
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import random

STREAM_URL = "https://kick.com/samutvv9"
NUM_NORMAL = 10
NUM_INCOGNITO = 10
VIEW_DURATION_MIN = 30  # minutos

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chrome_multi_viewer.log'),
        logging.StreamHandler()
    ]
)

def launch_viewer(incognito=False, bot_id=1):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-plugins')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36')
    if incognito:
        chrome_options.add_argument('--incognito')
    
    # Solo Chrome
    chrome_options.binary_location = "/usr/bin/google-chrome"
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        logging.info(f"Bot {bot_id} {'(Incógnito)' if incognito else '(Normal)'}: Abriendo stream...")
        driver.get(STREAM_URL)
        
        # Esperar a que cargue el stream
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "video"))
            )
            logging.info(f"Bot {bot_id}: Stream cargado")
        except TimeoutException:
            logging.warning(f"Bot {bot_id}: No se encontró el video, pero se mantiene la ventana")
        
        # Simular comportamiento humano básico
        start_time = time.time()
        duration_seconds = VIEW_DURATION_MIN * 60
        while time.time() - start_time < duration_seconds:
            # Scroll aleatorio
            scroll_amount = random.randint(-200, 200)
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(10, 30))
        
        logging.info(f"Bot {bot_id}: Terminó de ver el stream")
        driver.quit()
    except Exception as e:
        logging.error(f"Bot {bot_id}: Error - {str(e)}")

def main():
    threads = []
    logging.info(f"Iniciando {NUM_NORMAL} ventanas normales y {NUM_INCOGNITO} incógnito en Chrome...")
    
    # Lanzar normales
    for i in range(NUM_NORMAL):
        t = threading.Thread(target=launch_viewer, args=(False, i+1))
        t.start()
        threads.append(t)
        time.sleep(1)  # Pequeño delay para evitar sobrecarga
    # Lanzar incógnito
    for i in range(NUM_INCOGNITO):
        t = threading.Thread(target=launch_viewer, args=(True, NUM_NORMAL + i + 1))
        t.start()
        threads.append(t)
        time.sleep(1)
    
    # Esperar a que terminen todos
    for t in threads:
        t.join()
    logging.info("✅ Todos los bots han terminado")

if __name__ == "__main__":
    main() 