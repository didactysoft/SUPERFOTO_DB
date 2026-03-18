@echo off
title Compilador SuperFoto DB - ADSO
color 0A

echo ==========================================
echo    LIMPIANDO CARPETAS PREVIAS...
echo ==========================================
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

echo.
echo ==========================================
echo    VERIFICANDO ESTRUCTURA DE PROYECTO
echo ==========================================
if not exist assets (echo [!] ERROR: No falta la carpeta assets && pause && exit)
if not exist database (echo [!] ADVERTENCIA: No hay carpeta database inicial)

echo.
echo ==========================================
echo    INICIANDO COMPILACION CON PYINSTALLER
echo ==========================================
pyinstaller --noconfirm SuperFotoDB.spec

echo.
echo ==========================================
echo    PROCESO FINALIZADO
echo ==========================================
echo El ejecutable esta en la carpeta: dist\SuperFotoDB.exe
echo Recuerda que la carpeta 'database' debe estar al lado del .exe
pause