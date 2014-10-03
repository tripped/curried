# Flake8: noqa
from curry import curry

import sys
import inspect
from types import ModuleType


class _CurriedModule(ModuleType):
    """
    A wrapper around a module that curries all its functions.
    Yes, this is stupid. Shut up.
    """
    def __init__(self, module):
        for name, thing in inspect.getmembers(module):
            if inspect.isfunction(thing):
                try:
                    setattr(self, name, curry(thing))
                except ValueError:
                    pass
            else:
                setattr(self, name, thing)


class _ImportMangler(ModuleType):
    """
    This class is used to wrap this module itself, allowing
    us to override the behavior of "from curried import X".
    """
    def __init__(self, module):
        for attr in ['__builtins__', '__doc__', '__name__', '__package']:
            setattr(self, attr, getattr(module, attr, None))
        self.__path__ = []
        self.module = module

    def _wrap_import(self, name):
        from importlib import import_module
        return _CurriedModule(import_module(name))

    def __getattr__(self, name):
        if hasattr(self.module, name):
            return getattr(self.module, name)
        return self._wrap_import(name)


if __name__ != '__main__':
    self = sys.modules[__name__]
    sys.modules[__name__] = _ImportMangler(self)
