#!/usr/bin/env python3
"""
Kick Stream Viewer Bot - Versión Chromium/Brave
Bot automático para ver streams de Kick usando Chromium o Brave
"""

import time
import random
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('kick_bot.log'),
        logging.StreamHandler()
    ]
)

class KickViewerBot:
    def __init__(self, browser_type="chromium"):
        self.driver = None
        self.ua = UserAgent()
        self.browser_type = browser_type
        self.setup_driver()
        
    def setup_driver(self):
        """Configurar el driver con Chromium o Brave"""
        chrome_options = Options()
        
        # Opciones para evitar detección de bot
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # User agent aleatorio
        chrome_options.add_argument(f'--user-agent={self.ua.random}')
        
        # Opciones adicionales para simular comportamiento humano
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')  # Cargar más rápido
        
        # Configurar el navegador según el tipo
        if self.browser_type == "chromium":
            chrome_options.binary_location = "/usr/bin/chromium"
            logging.info("Configurando Chromium...")
        elif self.browser_type == "brave":
            # Intentar diferentes rutas de Brave
            brave_paths = [
                "/usr/bin/brave-browser",
                "/usr/bin/brave",
                "/opt/brave.com/brave/brave-browser",
                "/snap/bin/brave"
            ]
            brave_found = False
            for path in brave_paths:
                if os.path.exists(path):
                    chrome_options.binary_location = path
                    brave_found = True
                    logging.info(f"Brave encontrado en: {path}")
                    break
            
            if not brave_found:
                logging.warning("Brave no encontrado, usando Chromium como fallback")
                chrome_options.binary_location = "/usr/bin/chromium"
                self.browser_type = "chromium"
        else:
            logging.info("Usando Chrome por defecto...")
        
        try:
            # Configurar el driver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Ejecutar script para evitar detección
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            logging.info(f"Driver configurado exitosamente con {self.browser_type}")
            
        except Exception as e:
            logging.error(f"Error configurando driver: {str(e)}")
            raise
    
    def watch_stream_without_login(self, stream_url, watch_duration_minutes=30):
        """Ver un stream sin iniciar sesión"""
        try:
            logging.info(f"Viendo stream: {stream_url} sin login")
            
            # Ir al stream
            self.driver.get(stream_url)
            
            # Esperar a que cargue la página
            time.sleep(random.uniform(3, 5))
            
            # Verificar si el stream está en vivo
            try:
                live_indicator = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'LIVE')]"))
                )
                logging.info("Stream está en vivo")
            except TimeoutException:
                logging.warning("Stream no está en vivo o no se encontró el indicador")
            
            # Simular comportamiento de viewer humano
            start_time = time.time()
            duration_seconds = watch_duration_minutes * 60
            
            while time.time() - start_time < duration_seconds:
                # Simular movimientos aleatorios del mouse
                self.simulate_human_behavior()
                
                # Verificar si el stream sigue cargado
                if "kick.com" not in self.driver.current_url:
                    logging.warning("Página perdida, recargando...")
                    self.driver.get(stream_url)
                    time.sleep(random.uniform(2, 4))
                
                time.sleep(random.uniform(30, 60))  # Esperar entre 30-60 segundos
            
            logging.info(f"Terminó de ver el stream: {stream_url}")
            return True
            
        except Exception as e:
            logging.error(f"Error viendo stream: {str(e)}")
            return False
    
    def login(self, username, password):
        """Iniciar sesión en Kick"""
        try:
            logging.info(f"Iniciando sesión con: {username}")
            
            # Ir a la página de login
            self.driver.get("https://kick.com/login")
            time.sleep(random.uniform(2, 4))
            
            # Llenar formulario de login
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.send_keys(username)
            
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.send_keys(password)
            
            time.sleep(random.uniform(1, 2))
            
            # Hacer clic en el botón de login
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Esperar a que se complete el login
            time.sleep(random.uniform(3, 5))
            
            logging.info(f"Login exitoso: {username}")
            return True
            
        except Exception as e:
            logging.error(f"Error en login: {str(e)}")
            return False
    
    def watch_stream(self, stream_url, watch_duration_minutes=30):
        """Ver un stream específico"""
        try:
            logging.info(f"Viendo stream: {stream_url}")
            
            # Ir al stream
            self.driver.get(stream_url)
            
            # Esperar a que cargue la página
            time.sleep(random.uniform(3, 5))
            
            # Verificar si el stream está en vivo
            try:
                live_indicator = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'LIVE')]"))
                )
                logging.info("Stream está en vivo")
            except TimeoutException:
                logging.warning("Stream no está en vivo o no se encontró el indicador")
            
            # Simular comportamiento de viewer humano
            start_time = time.time()
            duration_seconds = watch_duration_minutes * 60
            
            while time.time() - start_time < duration_seconds:
                # Simular movimientos aleatorios del mouse
                self.simulate_human_behavior()
                
                # Verificar si el stream sigue cargado
                if "kick.com" not in self.driver.current_url:
                    logging.warning("Página perdida, recargando...")
                    self.driver.get(stream_url)
                    time.sleep(random.uniform(2, 4))
                
                time.sleep(random.uniform(30, 60))  # Esperar entre 30-60 segundos
            
            logging.info(f"Terminó de ver el stream: {stream_url}")
            return True
            
        except Exception as e:
            logging.error(f"Error viendo stream: {str(e)}")
            return False
    
    def simulate_human_behavior(self):
        """Simular comportamiento humano en la página"""
        try:
            # Scroll aleatorio
            scroll_amount = random.randint(-300, 300)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            
            # Pausa aleatoria
            time.sleep(random.uniform(1, 3))
            
            # Ocasionalmente hacer clic en elementos no importantes
            if random.random() < 0.1:  # 10% de probabilidad
                try:
                    # Buscar elementos clickeables que no sean importantes
                    elements = self.driver.find_elements(By.TAG_NAME, "button")
                    if elements:
                        random_element = random.choice(elements)
                        if random_element.is_displayed() and random_element.is_enabled():
                            random_element.click()
                            time.sleep(random.uniform(1, 2))
                except:
                    pass
                    
        except Exception as e:
            logging.debug(f"Error en simulación de comportamiento: {str(e)}")
    
    def watch_multiple_streams(self, streamers_list, watch_duration_minutes=30):
        """Ver múltiples streams en secuencia"""
        for streamer in streamers_list:
            logging.info(f"Cambiando a stream de: {streamer}")
            self.watch_stream(streamer, watch_duration_minutes)
            
            # Pausa entre streams
            pause_time = random.uniform(60, 180)  # 1-3 minutos
            logging.info(f"Pausa de {pause_time:.0f} segundos antes del siguiente stream")
            time.sleep(pause_time)
    
    def close(self):
        """Cerrar el driver"""
        if self.driver:
            self.driver.quit()
            logging.info("Driver cerrado")

def main():
    """Función principal"""
    print("🤖 Bot de Kick - Versión Chromium/Brave")
    print("=" * 50)
    
    # Preguntar qué navegador usar
    browser_choice = input("¿Qué navegador quieres usar? (chromium/brave): ").strip().lower()
    if browser_choice not in ["chromium", "brave"]:
        browser_choice = "chromium"
    
    # Preguntar si quiere usar cuenta
    use_account = input("¿Quieres usar una cuenta? (s/n): ").strip().lower() == 's'
    
    bot = KickViewerBot(browser_type=browser_choice)
    
    try:
        if use_account:
            # Con cuenta
            username = input("Usuario de Kick: ").strip()
            password = input("Password: ").strip()
            
            if bot.login(username, password):
                streamer = input("Nombre del streamer: ").strip()
                duration = int(input("Duración en minutos (default 30): ").strip() or "30")
                bot.watch_stream(streamer, duration)
            else:
                print("❌ Error en login")
        else:
            # Sin cuenta
            streamer = input("Nombre del streamer: ").strip()
            duration = int(input("Duración en minutos (default 30): ").strip() or "30")
            bot.watch_stream_without_login(streamer, duration)
            
    except KeyboardInterrupt:
        print("\n⏹️  Bot interrumpido por el usuario")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        bot.close()
        print("🔚 Bot cerrado")

if __name__ == "__main__":
    main() 