#!/bin/bash
set -e

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Mensaje de cabecera
clear
echo -e "${GREEN}Kick Chrome Multi-Viewer Installer${NC}"
echo "====================================="

# 1. Verificar Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 no está instalado. Instalando...${NC}"
    sudo apt update && sudo apt install -y python3
else
    echo -e "${GREEN}Python 3 encontrado${NC}"
fi

# 2. Verificar pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}pip3 no está instalado. Instalando...${NC}"
    sudo apt install -y python3-pip
else
    echo -e "${GREEN}pip3 encontrado${NC}"
fi

# 3. Verificar Google Chrome
if ! command -v google-chrome &> /dev/null; then
    echo -e "${RED}Google Chrome no está instalado. Instalando...${NC}"
    wget -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    sudo apt install -y /tmp/chrome.deb || sudo dpkg -i /tmp/chrome.deb
    rm /tmp/chrome.deb
else
    echo -e "${GREEN}Google Chrome encontrado${NC}"
fi

# 4. Instalar dependencias del sistema
sudo apt install -y unzip wget

# 5. Instalar dependencias Python
pip3 install --upgrade pip --break-system-packages
pip3 install selenium webdriver-manager fake-useragent --break-system-packages
pip3 install fake-useragent --break-system-packages

# 6. Descargar el script principal si no existe
if [ ! -f chrome_stealth_viewer.py ]; then
    echo -e "${RED}chrome_stealth_viewer.py no encontrado. Descargando...${NC}"
    wget -O chrome_stealth_viewer.py https://raw.githubusercontent.com/SamuelCba/bots/main/chrome_stealth_viewer.py
fi

# 7. Dar permisos de ejecución al script principal
chmod +x chrome_stealth_viewer.py

# 8. Ejecutar el bot automáticamente
echo -e "\n${GREEN}¡Listo! Ejecutando el bot...${NC}"
python3 chrome_stealth_viewer.py 