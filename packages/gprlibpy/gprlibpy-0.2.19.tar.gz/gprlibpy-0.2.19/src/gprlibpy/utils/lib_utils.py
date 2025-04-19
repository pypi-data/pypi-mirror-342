import importlib

def try_import(package_name):
    try:
        return importlib.import_module(package_name)
    except ImportError:
        return None