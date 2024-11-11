# -*- mode: python ; coding: utf-8 -*-
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, TYPE_CHECKING

SELF_PATH = str(Path(".").absolute())
if SELF_PATH not in sys.path:
    sys.path.insert(0, SELF_PATH)

from constants import WORKING_DIR, SITE_PACKAGES_PATH, DEFAULT_LANG

if TYPE_CHECKING:
    from PyInstaller.building.api import PYZ, EXE
    from PyInstaller.building.build_main import Analysis

# (source_path, dest_path, required)
to_add: list[tuple[Path, str, bool]] = [
    (Path("pickaxe.ico"), '.', True),  # icon file
    # SeleniumWire HTTPS/SSL cert file and key
    (Path(SITE_PACKAGES_PATH, "seleniumwire/ca.crt"), "./seleniumwire", False),
    (Path(SITE_PACKAGES_PATH, "seleniumwire/ca.key"), "./seleniumwire", False),
]
for lang_filepath in WORKING_DIR.joinpath("lang").glob("*.json"):
    to_add.append((lang_filepath, "lang", True))

# ensure the required to-be-added data exists
datas: list[tuple[Path, str]] = []
for source_path, dest_path, required in to_add:
    if source_path.exists():
        datas.append((source_path, dest_path))
    elif required:
        raise FileNotFoundError(str(source_path))

hooksconfig: dict[str, Any] = {}
binaries: list[tuple[Path, str]] = []
hiddenimports: list[str] = [
    "PIL._tkinter_finder",
    "setuptools._distutils.log",
    "setuptools._distutils.dir_util",
    "setuptools._distutils.file_util",
    "setuptools._distutils.archive_util",
]

block_cipher = None
a = Analysis(
    ["main.py"],
    pathex=[],
    datas=datas,
    excludes=[],
    hookspath=[],
    noarchive=False,
    runtime_hooks=[],
    binaries=binaries,
    cipher=block_cipher,
    hooksconfig=hooksconfig,
    hiddenimports=hiddenimports,
    win_private_assemblies=False,
    win_no_prefer_redirects=False,
)

# Exclude unneeded Linux libraries
excluded_binaries = [
    "libicudata.so.66",
    "libicuuc.so.66",
    "librsvg-2.so.2",
    # Direct library mappings
    'libavahi-client.so.3',
    'libavahi-common.so.3',
    'libbrotli.so.1',
    'libcolord.so.2',
    'libcups.so.2',
    'libdb.so.5.3',
    'libdconf.so.1',
    'libgmp.so.10',
    'libgnutls.so.30',
    'libgssapi-krb5.so.2',
    'libhogweed.so.5',
    'libicu.so.66',
    'libjson-glib-1.0.so.0',
    'libk5crypto.so.3',
    'libkrb5.so.3',
    'libkrb5support.so.0',
    'liblcms2.so.2',
    'libncursesw.so.6',
    'libnettle.so.7',
    'libp11-kit.so.0',
    'libpangoxft-1.0.so.0',
    'libpsl.so.5',
    'librest-0.7.so.0',
    'libsoup-2.4.so.1',
    'libsoup-gnome-2.4.so.1',
    'libsqlite3.so.0',
    'libtasn1.so.6',
    'libtiff.so.5',
    'libtinfo.so.6',
    'libunistring.so.2',
    'libwebp.so.6',
    'libxft.so.2',  # Since you'll ship your own version
    'libxml2.so.2',
    
    # Additional related libraries from package dependencies
    'libglib-networking.so',
    'libcolord.so',
    'libdconf.so',
    'libgssapi.so',
    
    # Wildcards to catch versioned libraries
    'libavahi-*.so.*',
    'libgmp.so.*',
    'libgnutls.so.*',
    'libkrb5*.so.*',
    'libhogweed.so.*',
    'libnettle.so.*',
    'libsoup*.so.*',
]
a.binaries = [b for b in a.binaries if b[0] not in excluded_binaries]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher, compress=True)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    upx=True,
    debug=False,
    strip=True,
    console=False,
    upx_exclude=[],
    target_arch=None,
    icon="pickaxe.ico",
    runtime_tmpdir=None,
    codesign_identity=None,
    entitlements_file=None,
    bootloader_ignore_signals=False,
    disable_windowed_traceback=False,
    name="Twitch Drops Miner (by DevilXD)",
)
