# PyInstaller specification for LinearLab
from PyInstaller.utils.hooks import collect_all
import shutil

datas = []
binaries = []
hiddenimports = []

project_modules = (
    "resources",
    "render_worker",
    "matrix_video_finder",
    "maths_syntaxer",
    "menuBar_texts",
    "matrix_multiplier",
    "Gauss_Jordan_Inverter",
    "trignometric_functions",
    "TwoD_vector_animator",
    "ThreeD_vector_animator",
    "unit_square_animator",
    "unit_cube_animator",
)
hiddenimports += project_modules

for package in (
    "manim",
    "manimpango",
    "manimpango.utils",
    "PySide6",
    "pydub",
    "pygments",
    "moderngl",
    "cairo",
):
    package_datas, package_binaries, package_hiddenimports = collect_all(package)
    datas += package_datas
    binaries += package_binaries
    hiddenimports += package_hiddenimports

for filename in (
    "main.ui",
    "unit_square.ui",
    "unit_cube.ui",
    "2D_vector.ui",
    "3D_vector.ui",
    "Unit_Square_GUI.py",
    "Unit_Cube_GUI.py",
    "2D_Vector_GUI.py",
    "3D_Vector_GUI.py",
    "resources.qrc",
    "icon.png",
):
    datas.append((filename, "."))

for executable_name in ("ffmpeg.exe", "ffprobe.exe"):
    executable_path = shutil.which(executable_name)
    if executable_path:
        binaries.append((executable_path, "."))

a = Analysis(
    ["main.py"],
    pathex=["."],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="LinearLab",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    icon="icon.ico",
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="LinearLab",
)
