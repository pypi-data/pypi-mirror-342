import importlib
import pkgutil

from layered_py.config_loader import Config

config = Config()
AUTOLOAD_PACKAGES = config.get_folder_array()

def load_all_modules():
    for pkg_name in AUTOLOAD_PACKAGES:
        try:
            pkg = importlib.import_module(pkg_name)
        except ModuleNotFoundError:
            continue  # Skip missing folders

        for module_info in pkgutil.walk_packages(pkg.__path__, prefix=pkg.__name__ + "."):
            importlib.import_module(module_info.name)