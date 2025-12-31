# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

# In your workflow you run PyInstaller with working-directory: backend,
# so Path.cwd() == backend/
project_dir = Path.cwd().resolve()

hiddenimports = collect_submodules("src")

# Bundle all .db files
datas = []
db_dir = project_dir / "data" / "db"
if db_dir.exists():
    for p in db_dir.glob("*.db"):
        datas.append((str(p), "data/db"))

# Optional: bundle an example file
ex = project_dir / "examples" / "example1.qs"
if ex.exists():
    datas.append((str(ex), "examples"))

a = Analysis(
    [str(project_dir / "main.py")],
    pathex=[str(project_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# IMPORTANT: onedir output -> exclude_binaries=True + COLLECT()
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
