#!/usr/bin/env python3
"""
Quick Multi-Bot Setup
Configuración rápida de múltiples bots
"""

from multi_bot_manager import MultiBotManager
import logging

def quick_multi_setup():
    """Configuración rápida de múltiples bots"""
    print("🤖 Quick Multi-Bot Setup para Kick")
    print("=" * 50)
    
    # Configurar logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    # Preguntar número de bots
    num_bots = int(input("¿Cuántos bots quieres crear? (1-10): ").strip())
    num_bots = max(1, min(10, num_bots))  # Limitar entre 1 y 10
    
    # Preguntar navegador
    print("\nNavegadores disponibles:")
    print("1. Chromium (recomendado)")
    print("2. Brave")
    print("3. Chrome")
    
    browser_choice = input("Elige navegador (1-3, default 1): ").strip()
    if browser_choice == "2":
        browser = "brave"
    elif browser_choice == "3":
        browser = "chrome"
    else:
        browser = "chromium"
    
    # Preguntar si usar cuenta
    use_account = input("\n¿Quieres usar una cuenta para todos los bots? (s/n): ").strip().lower() == 's'
    
    username = None
    password = None
    if use_account:
        username = input("Usuario de Kick: ").strip()
        password = input("Password: ").strip()
    
    # Crear manager
    manager = MultiBotManager(max_bots=num_bots)
    
    print(f"\n➕ Configurando {num_bots} bots...")
    
    # Configurar cada bot
    for i in range(num_bots):
        print(f"\n--- Bot {i+1} ---")
        stream_url = input(f"Link del stream para Bot {i+1}: ").strip()
        duration = int(input(f"Duración en minutos para Bot {i+1} (default 30): ").strip() or "30")
        
        bot_name = f"Bot_{i+1}"
        
        manager.add_bot_config(
            stream_url=stream_url,
            duration_minutes=duration,
            browser_type=browser,
            use_account=use_account,
            username=username,
            password=password,
            bot_name=bot_name
        )
    
    # Mostrar resumen
    print(f"\n📋 Resumen:")
    print(f"   Navegador: {browser}")
    print(f"   Bots: {num_bots}")
    print(f"   Modo: {'Con cuenta' if use_account else 'Sin cuenta'}")
    if use_account:
        print(f"   Usuario: {username}")
    
    print("\n🚀 Iniciando bots...")
    
    try:
        manager.run_all_bots()
    except KeyboardInterrupt:
        print("\n⏹️  Deteniendo bots...")
        manager.stop_all_bots()
    
    print("✅ Proceso completado")

if __name__ == "__main__":
    quick_multi_setup() 