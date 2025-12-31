# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

project_dir = Path(__file__).resolve().parent

hiddenimports = collect_submodules("src")

datas = [
    (str(project_dir / "data" / "db" / "quotes.db"), "data/db"),
    (str(project_dir / "data" / "db" / "quotes_test_abroad.db"), "data/db"),
    (str(project_dir / "data" / "db" / "quotes_test_native.db"), "data/db"),
    (str(project_dir / "examples" / "example1.qs"), "examples"),
]

a = Analysis(
    ["main.py"],
    pathex=[str(project_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
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
    [],
    exclude_binaries=True,
    name="quotescript_cli",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name="quotescript_cli",
)
