# -*- mode: python -*-
from kivy_deps import sdl2, glew
from kivy.tools.packaging.pyinstaller_hooks import get_deps_minimal, hookspath, runtime_hooks
block_cipher = None


a = Analysis(['kivy_py_inspect.py'],
             pathex=['.'],
             datas=[],
             hookspath=hookspath(),
             runtime_hooks=runtime_hooks(),
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False,
             **get_deps_minimal(audio=['audio_sdl2'], camera=None, clipboard=['clipboard_winctypes'], image=['img_sdl2'], spelling=None, text=['text_sdl2'], video=None, window=['window_sdl2']))
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz, Tree('.'),
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
          name='PyInspect',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
