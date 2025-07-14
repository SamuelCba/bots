#!/usr/bin/env python3
"""
Simple Multi-Bot para Kick
Todos los bots ven el mismo stream
"""

from multi_bot_manager import MultiBotManager
import logging

def simple_multi_bot():
    """Bot simple donde todos ven el mismo stream"""
    print("🤖 Simple Multi-Bot para Kick")
    print("=" * 40)
    
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
    
    # UN SOLO LINK PARA TODOS
    stream_url = input("\nLink del stream (todos los bots verán este): ").strip()
    duration = int(input("Duración en minutos (default 30): ").strip() or "30")
    
    # Crear manager
    manager = MultiBotManager(max_bots=num_bots)
    
    print(f"\n➕ Configurando {num_bots} bots para ver: {stream_url}")
    
    # Configurar todos los bots con el mismo stream
    for i in range(num_bots):
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
    print(f"   Stream: {stream_url}")
    print(f"   Bots: {num_bots}")
    print(f"   Navegador: {browser}")
    print(f"   Duración: {duration} minutos")
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
    simple_multi_bot() 