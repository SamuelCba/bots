#!/usr/bin/env python3
"""
Kick Stream Viewer Bot
Bot automático para ver streams de Kick
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
    def __init__(self):
        self.driver = None
        self.ua = UserAgent()
        self.setup_driver()
        
    def setup_driver(self):
        """Configurar el driver de Chrome con opciones para evitar detección"""
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
        chrome_options.add_argument('--disable-javascript')  # Opcional, para mayor velocidad
        
        # Configurar el driver - usar Chromium
        try:
            # Intentar usar Chromium directamente
            chrome_options.binary_location = "/usr/bin/chromium"
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            logging.warning(f"No se pudo usar Chromium: {e}")
            # Fallback a Chrome normal
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Ejecutar script para evitar detección
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        logging.info("Driver configurado exitosamente")
    
    def create_account(self, username, email, password):
        """Crear una cuenta en Kick"""
        try:
            logging.info(f"Intentando crear cuenta: {username}")
            
            # Ir a la página de registro
            self.driver.get("https://kick.com/signup")
            time.sleep(random.uniform(2, 4))
            
            # Llenar formulario de registro
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.send_keys(username)
            
            email_field = self.driver.find_element(By.NAME, "email")
            email_field.send_keys(email)
            
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.send_keys(password)
            
            # Simular comportamiento humano
            time.sleep(random.uniform(1, 2))
            
            # Hacer clic en el botón de registro
            signup_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            signup_button.click()
            
            # Esperar a que se complete el registro
            time.sleep(random.uniform(5, 8))
            
            logging.info(f"Cuenta creada exitosamente: {username}")
            return True
            
        except Exception as e:
            logging.error(f"Error al crear cuenta: {str(e)}")
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
    
    def watch_stream(self, streamer_username, watch_duration_minutes=30):
        """Ver un stream específico"""
        try:
            logging.info(f"Viendo stream de: {streamer_username}")
            
            # Ir al stream
            stream_url = f"https://kick.com/{streamer_username}"
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
            
            logging.info(f"Terminó de ver el stream de {streamer_username}")
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
    # Configuración
    STREAMERS = [
        "streamer1",  # Reemplaza con nombres reales de streamers
        "streamer2",
        "streamer3"
    ]
    
    # Credenciales (puedes usar variables de entorno)
    USERNAME = os.getenv("KICK_USERNAME", "tu_usuario")
    EMAIL = os.getenv("KICK_EMAIL", "tu_email@ejemplo.com")
    PASSWORD = os.getenv("KICK_PASSWORD", "tu_password")
    
    bot = KickViewerBot()
    
    try:
        # Crear cuenta (solo la primera vez)
        # bot.create_account(USERNAME, EMAIL, PASSWORD)
        
        # Login
        if bot.login(USERNAME, PASSWORD):
            # Ver streams
            bot.watch_multiple_streams(STREAMERS, watch_duration_minutes=30)
        else:
            logging.error("No se pudo hacer login")
            
    except KeyboardInterrupt:
        logging.info("Bot interrumpido por el usuario")
    except Exception as e:
        logging.error(f"Error general: {str(e)}")
    finally:
        bot.close()

if __name__ == "__main__":
    main() 