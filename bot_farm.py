#!/usr/bin/env python3
"""
Bot Farm para Kick
Ejecuta múltiples bots con diferentes configuraciones
"""

import json
import time
import random
from multi_bot_manager import MultiBotManager
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot_farm.log'),
        logging.StreamHandler()
    ]
)

class BotFarm:
    def __init__(self):
        self.managers = []
        self.farm_config = {
            "max_bots_per_manager": 3,
            "delay_between_managers": 30,  # segundos
            "total_managers": 2
        }
    
    def create_streamer_farm(self, streamers_list, bots_per_streamer=2):
        """Crear bots para múltiples streamers"""
        print(f"🏭 Creando Bot Farm para {len(streamers_list)} streamers")
        
        for i, streamer in enumerate(streamers_list):
            manager = MultiBotManager(max_bots=bots_per_streamer)
            
            for j in range(bots_per_streamer):
                bot_name = f"Farm_{streamer}_{j+1}"
                duration = random.randint(20, 40)  # Duración aleatoria
                
                manager.add_bot_config(
                    stream_url=f"https://kick.com/{streamer}",
                    duration_minutes=duration,
                    browser_type="chromium",
                    use_account=False,
                    bot_name=bot_name
                )
            
            self.managers.append(manager)
            logging.info(f"✅ Manager {i+1} creado para {streamer} con {bots_per_streamer} bots")
    
    def create_mixed_farm(self, configs):
        """Crear bots con configuraciones mixtas"""
        print(f"🏭 Creando Bot Farm mixto")
        
        manager = MultiBotManager(max_bots=len(configs))
        
        for i, config in enumerate(configs):
            bot_name = f"Mixed_Bot_{i+1}"
            
            manager.add_bot_config(
                stream_url=config["stream_url"],
                duration_minutes=config.get("duration", 30),
                browser_type=config.get("browser", "chromium"),
                use_account=config.get("use_account", False),
                username=config.get("username"),
                password=config.get("password"),
                bot_name=bot_name
            )
        
        self.managers.append(manager)
        logging.info(f"✅ Manager mixto creado con {len(configs)} bots")
    
    def run_farm(self):
        """Ejecutar toda la granja de bots"""
        if not self.managers:
            logging.error("No hay managers configurados")
            return
        
        print(f"🚀 Iniciando Bot Farm con {len(self.managers)} managers")
        
        try:
            for i, manager in enumerate(self.managers):
                print(f"\n🏭 Ejecutando Manager {i+1}/{len(self.managers)}")
                manager.run_all_bots()
                
                if i < len(self.managers) - 1:  # No esperar después del último
                    delay = self.farm_config["delay_between_managers"]
                    print(f"⏳ Esperando {delay} segundos antes del siguiente manager...")
                    time.sleep(delay)
                    
        except KeyboardInterrupt:
            print("\n⏹️  Deteniendo Bot Farm...")
            self.stop_farm()
    
    def stop_farm(self):
        """Detener toda la granja"""
        for manager in self.managers:
            manager.stop_all_bots()
        logging.info("✅ Bot Farm detenido")
    
    def save_farm_config(self, filename="farm_config.json"):
        """Guardar configuración de la granja"""
        config = {
            "farm_config": self.farm_config,
            "managers": []
        }
        
        for manager in self.managers:
            config["managers"].append(manager.bot_configs)
        
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)
        
        logging.info(f"💾 Configuración de granja guardada en {filename}")

def create_popular_streamers_farm():
    """Crear granja para streamers populares"""
    popular_streamers = [
        "xqc",
        "trainwreckstv", 
        "adinross",
        "destiny",
        "hasanabi"
    ]
    
    farm = BotFarm()
    farm.create_streamer_farm(popular_streamers, bots_per_streamer=2)
    return farm

def create_custom_farm():
    """Crear granja personalizada"""
    configs = [
        {
            "stream_url": "https://kick.com/xqc",
            "duration": 25,
            "browser": "chromium"
        },
        {
            "stream_url": "https://kick.com/trainwreckstv", 
            "duration": 30,
            "browser": "chromium"
        },
        {
            "stream_url": "https://kick.com/adinross",
            "duration": 20,
            "browser": "chromium"
        },
        {
            "stream_url": "https://kick.com/destiny",
            "duration": 35,
            "browser": "chromium"
        }
    ]
    
    farm = BotFarm()
    farm.create_mixed_farm(configs)
    return farm

def main():
    """Función principal del Bot Farm"""
    print("🏭 Bot Farm para Kick")
    print("=" * 30)
    print("1. Granja de streamers populares")
    print("2. Granja personalizada")
    print("3. Configuración interactiva")
    
    choice = input("\nElige opción (1-3): ").strip()
    
    if choice == "1":
        farm = create_popular_streamers_farm()
        farm.run_farm()
    elif choice == "2":
        farm = create_custom_farm()
        farm.run_farm()
    elif choice == "3":
        interactive_farm_setup()
    else:
        print("❌ Opción inválida")

def interactive_farm_setup():
    """Configuración interactiva de la granja"""
    print("\n🏭 Configuración Interactiva del Bot Farm")
    print("=" * 40)
    
    farm = BotFarm()
    
    # Configurar parámetros de la granja
    farm.farm_config["max_bots_per_manager"] = int(
        input("Máximo bots por manager (default 3): ").strip() or "3"
    )
    farm.farm_config["delay_between_managers"] = int(
        input("Delay entre managers en segundos (default 30): ").strip() or "30"
    )
    
    # Preguntar tipo de configuración
    print("\nTipos de configuración:")
    print("1. Lista de streamers (mismo número de bots por streamer)")
    print("2. Configuración mixta (diferentes configuraciones)")
    
    config_type = input("Elige tipo (1-2): ").strip()
    
    if config_type == "1":
        # Lista de streamers
        streamers_input = input("Streamers (separados por coma): ").strip()
        streamers = [s.strip() for s in streamers_input.split(",")]
        
        bots_per_streamer = int(
            input("Bots por streamer (default 2): ").strip() or "2"
        )
        
        farm.create_streamer_farm(streamers, bots_per_streamer)
        
    elif config_type == "2":
        # Configuración mixta
        configs = []
        
        while True:
            print(f"\n--- Configuración {len(configs) + 1} ---")
            stream_url = input("Link del stream (o 'fin' para terminar): ").strip()
            
            if stream_url.lower() == 'fin':
                break
                
            duration = int(input("Duración en minutos (default 30): ").strip() or "30")
            
            configs.append({
                "stream_url": stream_url,
                "duration": duration,
                "browser": "chromium"
            })
        
        if configs:
            farm.create_mixed_farm(configs)
    
    # Ejecutar granja
    if farm.managers:
        print(f"\n🚀 Iniciando granja con {len(farm.managers)} managers...")
        try:
            farm.run_farm()
        except KeyboardInterrupt:
            print("\n⏹️  Deteniendo granja...")
            farm.stop_farm()
    else:
        print("❌ No hay configuración válida")

if __name__ == "__main__":
    main() 