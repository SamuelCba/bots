#!/usr/bin/env python3
"""
Multi-Bot Manager para Kick
Gestiona múltiples bots que ven streams simultáneamente
"""

import threading
import time
import random
import logging
from kick_viewer_bot_chromium import KickViewerBot
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('multi_bot.log'),
        logging.StreamHandler()
    ]
)

class MultiBotManager:
    def __init__(self, max_bots=5):
        self.max_bots = max_bots
        self.active_bots = []
        self.bot_configs = []
        self.running = False
        
    def add_bot_config(self, stream_url, duration_minutes=30, browser_type="chromium", 
                      use_account=False, username=None, password=None, bot_name=None):
        """Agregar configuración de un bot"""
        if not bot_name:
            bot_name = f"Bot_{len(self.bot_configs) + 1}"
            
        config = {
            "bot_name": bot_name,
            "stream_url": stream_url,
            "duration_minutes": duration_minutes,
            "browser_type": browser_type,
            "use_account": use_account,
            "username": username,
            "password": password
        }
        
        self.bot_configs.append(config)
        logging.info(f"Configuración agregada para {bot_name}: {stream_url}")
        
    def run_single_bot(self, config):
        """Ejecutar un solo bot"""
        bot_name = config["bot_name"]
        logging.info(f"🚀 Iniciando {bot_name}")
        
        try:
            # Crear bot
            bot = KickViewerBot(browser_type=config["browser_type"])
            self.active_bots.append(bot)
            
            # Login si es necesario
            if config["use_account"] and config["username"] and config["password"]:
                if bot.login(config["username"], config["password"]):
                    logging.info(f"✅ {bot_name}: Login exitoso")
                    bot.watch_stream(config["stream_url"], config["duration_minutes"])
                else:
                    logging.error(f"❌ {bot_name}: Error en login")
            else:
                # Ver sin cuenta
                bot.watch_stream_without_login(config["stream_url"], config["duration_minutes"])
            
            logging.info(f"✅ {bot_name}: Sesión completada")
            
        except Exception as e:
            logging.error(f"❌ {bot_name}: Error - {str(e)}")
        finally:
            # Cerrar bot
            if bot in self.active_bots:
                self.active_bots.remove(bot)
            bot.close()
            logging.info(f"🔚 {bot_name}: Bot cerrado")
    
    def run_all_bots(self):
        """Ejecutar todos los bots simultáneamente"""
        if not self.bot_configs:
            logging.warning("No hay configuraciones de bots")
            return
            
        self.running = True
        logging.info(f"🚀 Iniciando {len(self.bot_configs)} bots simultáneamente")
        
        # Usar ThreadPoolExecutor para ejecutar bots en paralelo
        with ThreadPoolExecutor(max_workers=self.max_bots) as executor:
            # Enviar todos los bots
            future_to_bot = {
                executor.submit(self.run_single_bot, config): config["bot_name"] 
                for config in self.bot_configs
            }
            
            # Esperar a que terminen
            for future in as_completed(future_to_bot):
                bot_name = future_to_bot[future]
                try:
                    future.result()
                except Exception as e:
                    logging.error(f"❌ {bot_name}: Error inesperado - {str(e)}")
        
        self.running = False
        logging.info("🎉 Todos los bots han terminado")
    
    def stop_all_bots(self):
        """Detener todos los bots"""
        self.running = False
        logging.info("🛑 Deteniendo todos los bots...")
        
        for bot in self.active_bots[:]:  # Copiar lista para evitar errores
            try:
                bot.close()
                self.active_bots.remove(bot)
            except:
                pass
        
        logging.info("✅ Todos los bots detenidos")
    
    def save_config(self, filename="bot_configs.json"):
        """Guardar configuración en archivo"""
        with open(filename, 'w') as f:
            json.dump(self.bot_configs, f, indent=2)
        logging.info(f"💾 Configuración guardada en {filename}")
    
    def load_config(self, filename="bot_configs.json"):
        """Cargar configuración desde archivo"""
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                self.bot_configs = json.load(f)
            logging.info(f"📂 Configuración cargada desde {filename}")
            return True
        return False

def create_sample_config():
    """Crear configuración de ejemplo"""
    manager = MultiBotManager(max_bots=3)
    
    # Bot 1: Ver xQc sin cuenta
    manager.add_bot_config(
        stream_url="https://kick.com/xqc",
        duration_minutes=30,
        browser_type="chromium",
        use_account=False,
        bot_name="Bot_xQc"
    )
    
    # Bot 2: Ver Trainwreckstv sin cuenta
    manager.add_bot_config(
        stream_url="https://kick.com/trainwreckstv",
        duration_minutes=25,
        browser_type="chromium",
        use_account=False,
        bot_name="Bot_Trainwreck"
    )
    
    # Bot 3: Ver AdinRoss sin cuenta
    manager.add_bot_config(
        stream_url="https://kick.com/adinross",
        duration_minutes=20,
        browser_type="chromium",
        use_account=False,
        bot_name="Bot_AdinRoss"
    )
    
    return manager

def interactive_setup():
    """Configuración interactiva de bots"""
    print("🤖 Configurador de Multi-Bots para Kick")
    print("=" * 50)
    
    max_bots = int(input("Número máximo de bots simultáneos (default 3): ").strip() or "3")
    manager = MultiBotManager(max_bots=max_bots)
    
    while True:
        print(f"\n📋 Bots configurados: {len(manager.bot_configs)}")
        print("1. Agregar bot")
        print("2. Ver configuración actual")
        print("3. Ejecutar todos los bots")
        print("4. Guardar configuración")
        print("5. Cargar configuración")
        print("6. Salir")
        
        choice = input("\nElige opción (1-6): ").strip()
        
        if choice == "1":
            # Agregar bot
            print("\n➕ Agregando nuevo bot:")
            stream_url = input("Link del stream: ").strip()
            duration = int(input("Duración en minutos (default 30): ").strip() or "30")
            
            browser_choice = input("Navegador (chromium/brave/chrome, default chromium): ").strip()
            if not browser_choice:
                browser_choice = "chromium"
            
            use_account = input("¿Usar cuenta? (s/n, default n): ").strip().lower() == 's'
            
            username = None
            password = None
            if use_account:
                username = input("Usuario: ").strip()
                password = input("Password: ").strip()
            
            bot_name = input("Nombre del bot (opcional): ").strip()
            
            manager.add_bot_config(
                stream_url=stream_url,
                duration_minutes=duration,
                browser_type=browser_choice,
                use_account=use_account,
                username=username,
                password=password,
                bot_name=bot_name
            )
            
        elif choice == "2":
            # Ver configuración
            print("\n📋 Configuración actual:")
            for i, config in enumerate(manager.bot_configs, 1):
                print(f"{i}. {config['bot_name']}: {config['stream_url']} ({config['duration_minutes']} min)")
                
        elif choice == "3":
            # Ejecutar bots
            if manager.bot_configs:
                print(f"\n🚀 Ejecutando {len(manager.bot_configs)} bots...")
                try:
                    manager.run_all_bots()
                except KeyboardInterrupt:
                    print("\n⏹️  Deteniendo bots...")
                    manager.stop_all_bots()
            else:
                print("❌ No hay bots configurados")
                
        elif choice == "4":
            # Guardar configuración
            filename = input("Nombre del archivo (default bot_configs.json): ").strip() or "bot_configs.json"
            manager.save_config(filename)
            
        elif choice == "5":
            # Cargar configuración
            filename = input("Nombre del archivo (default bot_configs.json): ").strip() or "bot_configs.json"
            if manager.load_config(filename):
                print(f"✅ Configuración cargada: {len(manager.bot_configs)} bots")
            else:
                print("❌ Archivo no encontrado")
                
        elif choice == "6":
            print("👋 ¡Hasta luego!")
            break
            
        else:
            print("❌ Opción inválida")

def main():
    """Función principal"""
    print("🤖 Multi-Bot Manager para Kick")
    print("=" * 40)
    print("1. Configuración interactiva")
    print("2. Ejecutar configuración de ejemplo")
    print("3. Cargar configuración guardada")
    
    choice = input("\nElige opción (1-3): ").strip()
    
    if choice == "1":
        interactive_setup()
    elif choice == "2":
        manager = create_sample_config()
        print("🚀 Ejecutando configuración de ejemplo...")
        try:
            manager.run_all_bots()
        except KeyboardInterrupt:
            print("\n⏹️  Deteniendo bots...")
            manager.stop_all_bots()
    elif choice == "3":
        manager = MultiBotManager()
        if manager.load_config():
            print(f"🚀 Ejecutando {len(manager.bot_configs)} bots...")
            try:
                manager.run_all_bots()
            except KeyboardInterrupt:
                print("\n⏹️  Deteniendo bots...")
                manager.stop_all_bots()
        else:
            print("❌ No se encontró archivo de configuración")
    else:
        print("❌ Opción inválida")

if __name__ == "__main__":
    main() 