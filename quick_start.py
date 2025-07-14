#!/usr/bin/env python3
"""
Script de Inicio Rápido
Para probar el bot fácilmente
"""

from kick_viewer_bot import KickViewerBot
import logging

def quick_test():
    """Prueba rápida del bot"""
    print("🤖 Iniciando Bot de Kick - Prueba Rápida")
    print("=" * 50)
    
    # Configurar logging básico
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    # Crear bot
    bot = KickViewerBot()
    
    try:
        # Configuración de prueba
        username = input("Usuario de Kick: ").strip()
        password = input("Password: ").strip()
        streamer = input("Nombre del streamer a ver: ").strip()
        duration = input("Duración en minutos (default 10): ").strip()
        
        if not duration:
            duration = 10
        else:
            duration = int(duration)
        
        print(f"\n🎯 Configuración:")
        print(f"   Usuario: {username}")
        print(f"   Streamer: {streamer}")
        print(f"   Duración: {duration} minutos")
        print("\n⏳ Iniciando...")
        
        # Login
        if bot.login(username, password):
            print("✅ Login exitoso!")
            
            # Ver stream
            print(f"📺 Viendo stream de {streamer}...")
            if bot.watch_stream(streamer, duration):
                print("✅ Sesión completada!")
            else:
                print("❌ Error viendo el stream")
        else:
            print("❌ Error en login")
            
    except KeyboardInterrupt:
        print("\n⏹️  Bot interrumpido por el usuario")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        bot.close()
        print("🔚 Bot cerrado")

if __name__ == "__main__":
    quick_test() 