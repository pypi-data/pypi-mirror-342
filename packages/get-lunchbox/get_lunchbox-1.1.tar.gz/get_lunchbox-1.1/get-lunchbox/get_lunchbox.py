import importlib
def get_lunchbox(*modules):
    class Box:
        pass

    box = Box()

    for mod in modules:
        if isinstance(mod, tuple):
            module_path = mod[0]
            alias = mod[1] if len(mod) > 1 else module_path.split(".")[-1]
        else:
            raise ValueError("Modules must be passed as tuples")

        try:
            module = importlib.import_module(module_path)
            setattr(box, alias, module)
        except ImportError as e:
            print(f"Could not import {module_path}: {e}")

    return box
class LazyBox:
    def __init__(self, modules):
        self._module_defs = modules
        self._loaded_modules = {}

    def __getattr__(self, name):
        if name in self._loaded_modules:
            return self._loaded_modules[name]

        for module_path, alias in self._module_defs:
            if alias == name:
                import importlib
                mod = importlib.import_module(module_path)
                self._loaded_modules[name] = mod
                return mod

        raise AttributeError(f"No module alias '{name}' found.")

def get_lazy_lunchbox(*modules):
    return LazyBox(modules)