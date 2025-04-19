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