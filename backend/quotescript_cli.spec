# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

block_cipher = None

# PyInstaller provides:
# - SPEC: the spec file argument (e.g. "backend/quotescript_cli.spec" or "quotescript_cli.spec")
# - SPECPATH: path prefix to SPEC (directory part)
# Use these instead of __file__ (which may not exist in spec execution context).
spec_arg = globals().get("SPEC", "")
spec_path_prefix = globals().get("SPECPATH", "")

if spec_arg:
    # Anchor relative SPEC to the current working directory.
    spec_file = (Path.cwd() / Path(spec_arg)).resolve()
    project_dir = spec_file.parent
elif spec_path_prefix:
    project_dir = (Path.cwd() / Path(spec_path_prefix)).resolve()
else:
    project_dir = Path.cwd().resolve()

# Bundle DB files so the packaged exe can load them at runtime.
db_dir = project_dir / "data" / "db"
datas = []
if db_dir.exists():
    datas.extend([(str(p), "data/db") for p in db_dir.glob("*.db")])

a = Analysis(
    [str(project_dir / "main.py")],
    pathex=[str(project_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
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
    name="quotescript_cli",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)
