# -*- mode: python ; coding: utf-8 -*-
import sys

# pyinstaller --onefile --collect-data pygame_gui main.py


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[("data","data")],#[('data/Logo.png', 'data'), ("data/check.svg", "data")],
    hiddenimports=["pygame_gui"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=2,
)

pyz = PYZ(a.pure)

if (sys.platform.lower().strip() != "darwin"):
    splash = Splash('data/Logo.png',
                    binaries=a.binaries,
                    datas=a.datas,
                    text_pos=(10, 50),
                    text_size=12,
                    text_color='black')


options = [('v', None, 'OPTION')]
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    exclude_binaries=False,
    name='AutoClicker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['data/Logo.png']
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)


app = BUNDLE(coll,
         name='MeClickFast.app',
         icon="data/Logo.png",
         bundle_identifier=None)

