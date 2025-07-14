#!/usr/bin/env python3
"""
Script de Inicio Rápido - Versión Chromium/Brave
Para probar el bot fácilmente con Chromium o Brave
"""

from kick_viewer_bot_chromium import KickViewerBot
import logging

def quick_test():
    """Prueba rápida del bot con Chromium/Brave"""
    print("🤖 Bot de Kick - Prueba Rápida (Chromium/Brave)")
    print("=" * 60)
    
    # Configurar logging básico
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    # Preguntar navegador
    print("Navegadores disponibles:")
    print("1. Chromium (recomendado)")
    print("2. Brave")
    print("3. Chrome (fallback)")
    
    choice = input("Elige navegador (1-3, default 1): ").strip()
    
    if choice == "2":
        browser = "brave"
    elif choice == "3":
        browser = "chrome"
    else:
        browser = "chromium"
    
    print(f"\n🌐 Usando: {browser}")
    
    # Crear bot
    bot = KickViewerBot(browser_type=browser)
    
    try:
        # Preguntar si usar cuenta
        use_account = input("\n¿Quieres usar una cuenta? (s/n): ").strip().lower() == 's'
        
        if use_account:
            # Con cuenta
            username = input("Usuario de Kick: ").strip()
            password = input("Password: ").strip()
            
            print(f"\n🎯 Configuración:")
            print(f"   Navegador: {browser}")
            print(f"   Usuario: {username}")
            print(f"   Modo: Con cuenta")
            print("\n⏳ Iniciando...")
            
            # Login
            if bot.login(username, password):
                print("✅ Login exitoso!")
                
                # Ver stream
                stream_url = input("Link del stream a ver (ej: https://kick.com/xqc): ").strip()
                duration = input("Duración en minutos (default 10): ").strip()
                
                if not duration:
                    duration = 10
                else:
                    duration = int(duration)
                
                print(f"📺 Viendo stream: {stream_url} ...")
                if bot.watch_stream(stream_url, duration):
                    print("✅ Sesión completada!")
                else:
                    print("❌ Error viendo el stream")
            else:
                print("❌ Error en login")
        else:
            # Sin cuenta
            stream_url = input("Link del stream a ver (ej: https://kick.com/xqc): ").strip()
            duration = input("Duración en minutos (default 10): ").strip()
            
            if not duration:
                duration = 10
            else:
                duration = int(duration)
            
            print(f"\n🎯 Configuración:")
            print(f"   Navegador: {browser}")
            print(f"   Stream: {stream_url}")
            print(f"   Duración: {duration} minutos")
            print(f"   Modo: Sin cuenta")
            print("\n⏳ Iniciando...")
            
            # Ver stream sin login
            print(f"📺 Viendo stream: {stream_url} ...")
            if bot.watch_stream_without_login(stream_url, duration):
                print("✅ Sesión completada!")
            else:
                print("❌ Error viendo el stream")
            
    except KeyboardInterrupt:
        print("\n⏹️  Bot interrumpido por el usuario")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        bot.close()
        print("🔚 Bot cerrado")

if __name__ == "__main__":
    quick_test() 