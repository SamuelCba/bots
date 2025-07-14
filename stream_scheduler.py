#!/usr/bin/env python3
"""
Programador de Streams para Kick
Permite programar múltiples sesiones de visualización
"""

import schedule
import time
import threading
from datetime import datetime, timedelta
from kick_viewer_bot import KickViewerBot
from config import STREAMERS, BOT_CONFIG, ACCOUNT_CONFIG
import logging

class StreamScheduler:
    def __init__(self):
        self.active_bots = []
        self.schedule_running = False
        
    def start_viewing_session(self, streamers=None, duration_minutes=None):
        """Iniciar una sesión de visualización"""
        if streamers is None:
            streamers = STREAMERS
            
        if duration_minutes is None:
            duration_minutes = BOT_CONFIG["watch_duration_minutes"]
            
        def run_session():
            bot = KickViewerBot()
            try:
                # Login
                if bot.login(ACCOUNT_CONFIG["username"], ACCOUNT_CONFIG["password"]):
                    logging.info(f"Iniciando sesión de visualización: {streamers}")
                    bot.watch_multiple_streams(streamers, duration_minutes)
                else:
                    logging.error("No se pudo hacer login para la sesión programada")
            except Exception as e:
                logging.error(f"Error en sesión programada: {str(e)}")
            finally:
                bot.close()
                if bot in self.active_bots:
                    self.active_bots.remove(bot)
        
        # Ejecutar en un hilo separado
        thread = threading.Thread(target=run_session)
        thread.daemon = True
        thread.start()
        
        logging.info(f"Sesión programada iniciada: {streamers}")
    
    def schedule_daily_sessions(self, times_list):
        """Programar sesiones diarias en horarios específicos"""
        for time_str in times_list:
            schedule.every().day.at(time_str).do(self.start_viewing_session)
            logging.info(f"Sesión programada diariamente a las {time_str}")
    
    def schedule_interval_sessions(self, interval_hours=4):
        """Programar sesiones cada X horas"""
        schedule.every(interval_hours).hours.do(self.start_viewing_session)
        logging.info(f"Sesiones programadas cada {interval_hours} horas")
    
    def run_scheduler(self):
        """Ejecutar el programador"""
        self.schedule_running = True
        logging.info("Programador iniciado")
        
        while self.schedule_running:
            schedule.run_pending()
            time.sleep(60)  # Revisar cada minuto
    
    def stop_scheduler(self):
        """Detener el programador"""
        self.schedule_running = False
        logging.info("Programador detenido")

def main():
    """Función principal del programador"""
    scheduler = StreamScheduler()
    
    # Ejemplo: Programar sesiones diarias
    daily_times = ["10:00", "14:00", "18:00", "22:00"]
    scheduler.schedule_daily_sessions(daily_times)
    
    # Ejemplo: Programar sesiones cada 6 horas
    scheduler.schedule_interval_sessions(6)
    
    try:
        scheduler.run_scheduler()
    except KeyboardInterrupt:
        logging.info("Programador interrumpido por el usuario")
        scheduler.stop_scheduler()

if __name__ == "__main__":
    main() 