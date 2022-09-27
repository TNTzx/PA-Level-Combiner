# -*- mode: python ; coding: utf-8 -*-


import os


block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

main_tcl_path = os.path.join(os.path.expanduser("~"), r"AppData\Local\Programs\Python\Python310\tcl")
tcl_paths = {
    prefix: os.path.join(main_tcl_path, extra_path)
    for prefix, extra_path in [
        ("tcl", "tcl8.6"),
        ("tk", "tk8.6")
    ]
}

for prefix, path in tcl_paths.items():
    a.datas += Tree(path, prefix=prefix)


pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)


exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="PA Level Combiner",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
