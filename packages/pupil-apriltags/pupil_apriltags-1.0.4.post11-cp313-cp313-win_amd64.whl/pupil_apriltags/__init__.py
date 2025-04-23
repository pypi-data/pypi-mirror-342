

""""""# start delvewheel patch
def _delvewheel_init_patch_1_1_1():
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'pupil_apriltags.libs'))
    is_pyinstaller = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
    if not is_pyinstaller or os.path.isdir(libs_dir):
        os.add_dll_directory(libs_dir)


_delvewheel_init_patch_1_1_1()
del _delvewheel_init_patch_1_1_1
# end delvewheel patch

try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:
    from importlib_metadata import PackageNotFoundError, version

try:
    __version__ = version("pupil-apriltags")
except PackageNotFoundError:
    # package is not installed
    pass

from .bindings import Detection, Detector

__all__ = ["Detector", "Detection"]
