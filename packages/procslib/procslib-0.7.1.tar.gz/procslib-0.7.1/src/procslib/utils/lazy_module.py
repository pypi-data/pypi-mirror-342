import importlib
from types import ModuleType


class _LazyModule(ModuleType):
    def __init__(self, name, module_file, import_structure):
        super().__init__(name)
        self._import_structure = import_structure
        self.__file__ = module_file
        self.__package__ = name
        self._modules = {}

    def __getattr__(self, item):
        if item in self._import_structure:
            module_name = self._import_structure[item]
            if module_name not in self._modules:
                self._modules[module_name] = importlib.import_module(module_name)
            return getattr(self._modules[module_name], item)
        raise AttributeError(f"Module '{self.__name__}' has no attribute '{item}'")

    def __dir__(self):
        return list(self._import_structure.keys())
