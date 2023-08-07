from os import remove, system
from os.path import isdir
from subprocess import call
from shutil import rmtree, copy, copytree

NAME = 'DDS Viewer'
LIBS = []
BUILD_SPEC_FN = 'build.spec'

build_spec = "# -*- mode: python ; coding: utf-8 -*-\n" \
             "\n" \
             f"NAME = '{NAME}'\n" \
             "\n" \
             "block_cipher = None\n" \
             "\n" \
             "a = Analysis(\n" \
             "    ['main.py'],\n" \
             "    pathex=[],\n" \
             "    binaries=[],\n" \
             "    datas=[],\n" \
             "    hiddenimports=[],\n" \
             "    hookspath=[],\n" \
             "    hooksconfig={},\n" \
             "    runtime_hooks=[],\n" \
             "    excludes=[],\n" \
             "    win_no_prefer_redirects=False,\n" \
             "    win_private_assemblies=False,\n" \
             "    cipher=block_cipher,\n" \
             "    noarchive=False,\n" \
             ")\n" \
             "pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)\n" \
             "\n" \
             "exe = EXE(\n" \
             "    pyz,\n" \
             "    a.scripts,\n" \
             "    [],\n" \
             "    exclude_binaries=True,\n" \
             "    name=NAME,\n" \
             "    debug=False,\n" \
             "    bootloader_ignore_signals=False,\n" \
             "    strip=False,\n" \
             "    upx=True,\n" \
             "    console=False,\n" \
             "    disable_windowed_traceback=False,\n" \
             "    argv_emulation=False,\n" \
             "    target_arch=None,\n" \
             "    codesign_identity=None,\n" \
             "    entitlements_file=None,\n" \
             "    icon=['icon.ico'],\n" \
             ")\n" \
             "coll = COLLECT(\n" \
             "    exe,\n" \
             "    a.binaries,\n" \
             "    a.zipfiles,\n" \
             "    a.datas,\n" \
             "    strip=False,\n" \
             "    upx=True,\n" \
             "    upx_exclude=[],\n" \
             "    name=NAME,\n" \
             ")\n"

for _ in ['dist', 'build']:
    try:
        rmtree(_)
    except BaseException:
        pass

# Create Pyinstaller Build File
with open(BUILD_SPEC_FN, 'w') as file:
    file.write(build_spec)

# Start Building
system(f'pyinstaller {BUILD_SPEC_FN}')

# Copy Files
for _ in LIBS:
    try:
        if isdir(_):
            copytree(_, f'dist/{NAME}/{_}')
        else:
            copy(_, f'dist/{NAME}/{_}')
    except BaseException:
        pass

rmtree('build')
remove(BUILD_SPEC_FN)

# call(f'dist/{NAME}/{NAME}.exe')
