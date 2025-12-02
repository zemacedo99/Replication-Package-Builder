# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src\\app.py'],
    pathex=['src'],
    binaries=[],
    datas=[('src\\templates', 'templates'), ('src\\static', 'static'), ('src\\data_results', 'data_results'), ('src\\queries', 'queries'), ('src\\data', 'data'), ('src\\search', 'search')],
    hiddenimports=['flask', 'pandas', 'matplotlib', 'seaborn', 'wordcloud', 'PIL', 'fpdf', 'bibtexparser', 'requests'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='replication_package_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='replication_package_app',
)
