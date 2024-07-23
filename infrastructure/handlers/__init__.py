import os
from types import ModuleType
from typing import Iterator


class Handlers:
    __handlers_base_path = ("infrastructure", "handlers")
    __ignored = ("__init__.py", "__pycache__", "schemas")

    @classmethod
    def __all_module_names(cls) -> list:
        return list(
            filter(
                lambda module: module not in cls.__ignored,
                os.listdir("/".join(cls.__handlers_base_path)),
            )
        )

    @classmethod
    def __module_namespace(cls, handler_name: str) -> str:
        return "{}.{}".format(".".join(cls.__handlers_base_path), handler_name)

    @classmethod
    def iterator(cls) -> Iterator[ModuleType]:
        for module in cls.__all_module_names():
            import importlib

            handler = importlib.import_module(cls.__module_namespace(module[:-3]))
            yield handler

    @classmethod
    def modules(cls) -> map:
        return map(
            lambda module: cls.__module_namespace(module[:-3]), cls.__all_module_names()
        )
