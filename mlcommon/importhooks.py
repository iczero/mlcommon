import importlib.abc
import sys
from typing import Self

class LoaderWrapper:
    def __init__(self, wrapped, hook_after_exec=None):
        self._wrapped = wrapped
        self.hook_after_exec = hook_after_exec

    def exec_module(self, module):
        self._wrapped.exec_module(module)
        if self.hook_after_exec is not None:
            self.hook_after_exec(module)

    def __getattr__(self, name):
        "default dispatcher"
        return getattr(self._wrapped, name)

class ImportHooks(importlib.abc.MetaPathFinder):
    def __init__(self):
        super().__init__()
        self.hooks = {}

    @classmethod
    def register(cls) -> Self:
        hooks = cls()
        sys.meta_path.insert(0, hooks)
        return hooks

    def hook_after_load(self, fullname):
        "Decorator to hook module after load"
        def _hook_after_load_decorator(hook):
            self.hooks[fullname] = hook
        return _hook_after_load_decorator

    def try_find_spec_after(self, fullname, path, target):
        "Attempt to obtain a spec from the other meta finders"
        seen_self = False
        for finder in sys.meta_path:
            if not seen_self:
                # don't run any finders before ourselves
                if finder is self:
                    # will resume after position
                    seen_self = True
                continue

            spec = finder.find_spec(fullname, path, target)
            if spec is not None:
                return spec

        if not seen_self:
            raise RuntimeError('could not find self on sys.meta_path')

        return None

    def find_spec(self, fullname, path, target=None):
        hook = self.hooks.get(fullname)
        if hook is not None:
            spec = self.try_find_spec_after(fullname, path, target)
            if spec is None:
                # hooked module does not exist
                return None

            wrapped_loader = LoaderWrapper(spec.loader, hook_after_exec=hook)
            spec.loader = wrapped_loader
            return spec

        return None
