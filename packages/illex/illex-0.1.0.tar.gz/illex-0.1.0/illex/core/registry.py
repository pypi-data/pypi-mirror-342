import importlib


class Registry(dict):
    def __getitem__(self, tag):
        ref = super().__getitem__(tag)
        if isinstance(ref, str):
            mod_name, func_name = ref.rsplit(".", 1)
            return getattr(importlib.import_module(mod_name), func_name)
        return ref


registry = Registry()
