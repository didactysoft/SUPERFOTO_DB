# -*- mode: python ; coding: utf-8 -*-
import os
import sys
import customtkinter
from PyInstaller.utils.hooks import collect_all

# 1. Rutas de librerías críticas
ctk_path = os.path.dirname(customtkinter.__file__)

# 2. Recolección automática de dependencias complejas (Babel y TkCalendar)
datas_babel, binaries_babel, hidden_babel = collect_all('babel')
datas_tkcal, binaries_tkcal, hidden_tkcal = collect_all('tkcalendar')

# 3. Definición de la estructura del paquete
# Agregamos los scripts como DATOS para que runpy los vea en _MEIPASS
datas = [
    ('assets', 'assets'), 
    ('modules', 'modules'), 
    ('database', 'database'), 
    ('login.py', '.'), 
    ('mainapp.py', '.'),
    (ctk_path, 'customtkinter') 
]

# Unimos todo lo recolectado
datas += datas_babel + datas_tkcal
binaries = binaries_babel + binaries_tkcal

# 4. Hidden imports para evitar que falten librerías en el local de Pamplona
hidden_imports = hidden_babel + hidden_tkcal + [
    'PIL._imagingtk', 
    'PIL._tkinter_finder',
    'babel.numbers',
    'sqlite3',
    'runpy'
]

block_cipher = None

a = Analysis(
    ['splashScreen.py'], # Punto de entrada único
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SuperFotoDB',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True, # Ponlo en True si necesitas ver errores de consola en la entrega
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # Asegúrate de que el icono exista en assets o quita esta línea
    icon='assets/logo.ico' if os.path.exists('assets/logo.ico') else None 
)