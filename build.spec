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

excludes = [
    'unittest', 'pydoc', 'doctest',
    'readline', 'pdb', 'pygettext3',
    'normalizer', 'valgrind',
    # From AppImageBuilder exclusions
    'adwaita_icon_theme',
    'dconf', 'glib_networking',
    'gsettings_desktop_schemas',
    'hicolor_icon_theme',
    'humanity_icon_theme',
    'colord', 'cups', 
    'json_glib', 'pango',
    'soup', 'sqlite3',
    'webp', 'xml',
    # Additional Python modules we can safely exclude
    'test', 'distutils', 'lib2to3',
    'tiff', 'tcl.test', 'tk.test',
    # Remove AppIndicator
    'gi', 'gi.repository.Gtk',
    'gi.repository.GObject',
    'gi.repository.AppIndicator3'
]

block_cipher = None
a = Analysis(
    ["main.py"],
    pathex=[],
    datas=datas,
    excludes=excludes,
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
    'libavahi-client.so.3',
    'libavahi-common.so.3',
    'libbrotli.so.1',
    'libcolord.so.2',
    'libcups.so.2',
    'libdb5.3.so',
    'libdconf.so.1',
    'libgmp.so.10',
    'libgnutls.so.30',
    'libhogweed.so.5',
    'libicu.so.66',
    'libjson-glib-1.0.so.0',
    'libk5crypto.so.3',
    'libkrb5.so.3',
    'liblcms2.so.2',
    'libncursesw.so.6',
    'libnettle.so.7',
    'libp11-kit.so.0',
    'libpangoxft-1.0.so.0',
    'libpsl.so.5',
    'librest-0.7.so.0',
    'libsoup-2.4.so.1',
    'libsqlite3.so.0',
    'libtasn1.so.6',
    'libtiff.so.5',
    'libtinfo.so.6',
    'libunistring.so.2',
    'libwebp.so.6',
    'libxml2.so.2',
    'libappindicator3.so.1',
    'libgirepository-1.0.so',
    'libgtk-3.so.0',
    'libgdk-3.so.0',
    'libatk-1.0.so.0',
    'libgdk_pixbuf-2.0.so.0',
    'libgio-2.0.so.0',
    'libgobject-2.0.so.0',
    'libglib-2.0.so.0'
]
a.binaries = [b for b in a.binaries if b[0] not in excluded_binaries]

# Keep only essential Tcl/Tk files based on runtime env vars in AppImageBuilder
tcl_tk_paths = {
    'tcl8.6',  # Based on TCL_LIBRARY
    'tk8.6',   # Based on TK_LIBRARY and TKPATH
    'tcltk'    # Additional Tcl/Tk files
}

a.datas = [x for x in a.datas if not x[0].startswith(('tcl', 'tk')) or 
           any(path in x[0] for path in tcl_tk_paths)]

# Remove other excluded paths from AppImageBuilder
excluded_paths = [
    'normalizer',
    'pdb3',
    'py3',
    'pydoc',
    'pygettext3',
    'valgrind',
    'glib-2.0',
    'gtk-3.0',
    'themes',
    'pixmaps',
    # Remove AppIndicator related paths
    'gi_typelibs',
    'gobject-introspection-1.0'
]

a.datas = [x for x in a.datas if not any(path in x[0] for path in excluded_paths)]

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
