# Bot Automático para Kick Streams

Un bot inteligente que automáticamente ve streams de Kick, simulando comportamiento humano para evitar detección.

## 🚀 Características

- ✅ Visualización automática de streams
- ✅ Simulación de comportamiento humano
- ✅ Programación de sesiones de visualización
- ✅ Rotación de User Agents
- ✅ Múltiples cuentas soportadas
- ✅ Logging detallado
- ✅ Configuración flexible

## 📋 Requisitos

- Python 3.8+
- Google Chrome
- Conexión a internet estable

## 🛠️ Instalación

1. **Clonar o descargar el proyecto**
```bash
git clone <tu-repositorio>
cd kick-viewer-bot
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno**
```bash
cp env_example.txt .env
# Editar .env con tus credenciales
```

## ⚙️ Configuración

### Archivo .env
```env
KICK_USERNAME=tu_usuario_aqui
KICK_EMAIL=tu_email@ejemplo.com
KICK_PASSWORD=tu_password_aqui
```

### Archivo config.py
Edita `config.py` para personalizar:
- Lista de streamers a ver
- Duración de visualización
- Configuración del navegador
- Comportamiento del bot

## 🎯 Uso

### Uso Básico
```bash
python kick_viewer_bot.py
```

### Con Programador
```bash
python stream_scheduler.py
```

### Ejemplo de Uso Personalizado
```python
from kick_viewer_bot import KickViewerBot

bot = KickViewerBot()

# Login
bot.login("tu_usuario", "tu_password")

# Ver un stream específico
bot.watch_stream("streamer_name", watch_duration_minutes=30)

# Ver múltiples streams
streamers = ["streamer1", "streamer2", "streamer3"]
bot.watch_multiple_streams(streamers, watch_duration_minutes=20)

bot.close()
```

## 📊 Funcionalidades

### 1. Bot Principal (`kick_viewer_bot.py`)
- Creación automática de cuentas
- Login automático
- Visualización de streams
- Simulación de comportamiento humano
- Manejo de errores

### 2. Programador (`stream_scheduler.py`)
- Programación de sesiones diarias
- Sesiones por intervalos
- Múltiples sesiones simultáneas
- Control de horarios

### 3. Configuración (`config.py`)
- Gestión centralizada de configuraciones
- Listas de streamers
- Configuración del navegador
- Parámetros del bot

## 🔧 Configuración Avanzada

### Cambiar Lista de Streamers
Edita `config.py`:
```python
STREAMERS = [
    "tu_streamer_favorito",
    "otro_streamer",
    # Agrega más aquí
]
```

### Configurar Duración de Visualización
```python
BOT_CONFIG = {
    "watch_duration_minutes": 45,  # Cambiar duración
    "pause_between_streams": (120, 300),  # Pausa entre streams
}
```

### Modo Headless (sin interfaz gráfica)
```python
BROWSER_CONFIG = {
    "headless": True,  # Ejecutar sin ventana
}
```

## 📝 Logs

El bot genera logs detallados en:
- `kick_bot.log` - Archivo de logs
- Consola - Logs en tiempo real

## ⚠️ Advertencias

1. **Uso Responsable**: Este bot es para fines educativos. Úsalo responsablemente.
2. **Términos de Servicio**: Respeta los términos de servicio de Kick.
3. **Detección**: Aunque el bot simula comportamiento humano, existe riesgo de detección.
4. **Límites**: No abuses del sistema con demasiadas cuentas o sesiones.

## 🐛 Solución de Problemas

### Error: "ChromeDriver not found"
```bash
pip install --upgrade webdriver-manager
```

### Error: "Element not found"
- Verifica que los nombres de streamers sean correctos
- Asegúrate de que los streams estén en vivo

### Error: "Login failed"
- Verifica credenciales en `.env`
- Asegúrate de que la cuenta existe

## 📈 Mejoras Futuras

- [ ] Soporte para múltiples navegadores
- [ ] Integración con proxies
- [ ] Dashboard web para monitoreo
- [ ] API REST para control remoto
- [ ] Análisis de estadísticas de streams

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es para fines educativos. Úsalo responsablemente.

## ⚡ Uso Rápido

1. Instala dependencias: `pip install -r requirements.txt`
2. Configura `.env` con tus credenciales
3. Edita `config.py` con tus streamers favoritos
4. Ejecuta: `python kick_viewer_bot.py`

¡Listo! El bot comenzará a ver streams automáticamente. 