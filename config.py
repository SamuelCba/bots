"""
Configuración del Bot de Kick
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de la cuenta
ACCOUNT_CONFIG = {
    "username": os.getenv("KICK_USERNAME", "bot_viewer_123"),
    "email": os.getenv("KICK_EMAIL", "bot@example.com"),
    "password": os.getenv("KICK_PASSWORD", "password123")
}

# Lista de streamers para ver
STREAMERS = [
    "xqc",           # Ejemplo de streamer popular
    "trainwreckstv", # Otro ejemplo
    "adinross",      # Otro ejemplo
    # Agrega más streamers aquí
]

# Configuración del bot
BOT_CONFIG = {
    "watch_duration_minutes": 30,  # Duración de cada stream en minutos
    "pause_between_streams": (60, 180),  # Pausa entre streams (min, max) en segundos
    "human_behavior_simulation": True,
    "auto_refresh": True,
    "max_concurrent_sessions": 1
}

# Configuración del navegador
BROWSER_CONFIG = {
    "headless": False,  # True para ejecutar sin interfaz gráfica
    "disable_images": True,
    "disable_javascript": False,
    "user_agent_rotation": True,
    "proxy_enabled": False,
    "proxy_list": []  # Lista de proxies si los tienes
}

# Configuración de logging
LOGGING_CONFIG = {
    "level": "INFO",
    "file": "kick_bot.log",
    "format": "%(asctime)s - %(levelname)s - %(message)s"
} 