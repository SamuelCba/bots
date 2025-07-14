#!/usr/bin/env python3
"""
One Link Bot Farm
Granja de bots que todos ven el mismo stream
"""

from multi_bot_manager import MultiBotManager
import logging
import random

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('one_link_farm.log'),
        logging.StreamHandler()
    ]
)

class OneLinkFarm:
    def __init__(self):
        self.managers = []
        self.stream_url = None
        self.total_bots = 0
        
    def setup_farm(self, stream_url, total_bots=10, bots_per_manager=3):
        """Configurar granja con un solo link"""
        self.stream_url = stream_url
        self.total_bots = total_bots
        
        print(f"🏭 Configurando One Link Farm")
        print(f"   Stream: {stream_url}")
        print(f"   Total bots: {total_bots}")
        print(f"   Bots por manager: {bots_per_manager}")
        
        # Calcular cuántos managers necesitamos
        num_managers = (total_bots + bots_per_manager - 1) // bots_per_manager
        
        for i in range(num_managers):
            manager = MultiBotManager(max_bots=bots_per_manager)
            
            # Calcular cuántos bots en este manager
            bots_in_this_manager = min(bots_per_manager, total_bots - i * bots_per_manager)
            
            for j in range(bots_in_this_manager):
                bot_name = f"Farm_Bot_{i+1}_{j+1}"
                duration = random.randint(25, 45)  # Duración aleatoria
                
                manager.add_bot_config(
                    stream_url=stream_url,
                    duration_minutes=duration,
                    browser_type="chromium",
                    use_account=False,
                    bot_name=bot_name
                )
            
            self.managers.append(manager)
            logging.info(f"✅ Manager {i+1} creado con {bots_in_this_manager} bots")
    
    def run_farm(self):
        """Ejecutar toda la granja"""
        if not self.managers:
            logging.error("No hay managers configurados")
            return
        
        print(f"🚀 Iniciando One Link Farm con {len(self.managers)} managers")
        print(f"📺 Todos viendo: {self.stream_url}")
        
        try:
            for i, manager in enumerate(self.managers):
                print(f"\n🏭 Ejecutando Manager {i+1}/{len(self.managers)}")
                manager.run_all_bots()
                
                if i < len(self.managers) - 1:  # No esperar después del último
                    delay = random.randint(10, 30)
                    print(f"⏳ Esperando {delay} segundos antes del siguiente manager...")
                    import time
                    time.sleep(delay)
                    
        except KeyboardInterrupt:
            print("\n⏹️  Deteniendo One Link Farm...")
            self.stop_farm()
    
    def stop_farm(self):
        """Detener toda la granja"""
        for manager in self.managers:
            manager.stop_all_bots()
        logging.info("✅ One Link Farm detenido")

def main():
    """Función principal"""
    print("🏭 One Link Bot Farm para Kick")
    print("=" * 40)
    
    # Configuración
    stream_url = input("Link del stream (todos los bots verán este): ").strip()
    total_bots = int(input("Número total de bots (default 10): ").strip() or "10")
    bots_per_manager = int(input("Bots por manager (default 3): ").strip() or "3")
    
    # Crear y ejecutar granja
    farm = OneLinkFarm()
    farm.setup_farm(stream_url, total_bots, bots_per_manager)
    farm.run_farm()

if __name__ == "__main__":
    main() 