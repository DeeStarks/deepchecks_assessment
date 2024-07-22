import os

from types import ModuleType
from typing import Iterator

from domain.events.interaction import LogInteractionEvent


class Events:
    __events_base_path = ("infrastructure", "events")
    __ignored = ("__init__.py", "__pycache__", "runners")

    @classmethod
    def __all_module_names(cls) -> list:
        return list(
            filter(
                lambda module: module not in cls.__ignored,
                os.listdir("/".join(cls.__events_base_path))
            )
        )

    @classmethod
    def __module_namespace(cls, event_name: str) -> str:
        return "{}.{}".format(".".join(cls.__events_base_path), event_name)

    @classmethod
    def modules(cls) -> map:
        return map(
            lambda module: cls.__module_namespace(module[:-3]), cls.__all_module_names()
        )

    # REGISTER EVENTS HERE AS STATIC METHODS
    # the reason for having them registered here is to have a single source of truth
    # for all events in the application
    # this also prevents import cycles in the dependency injector container as events
    # inject their dependencies from the container
    @staticmethod
    def log_interaction_queue() -> LogInteractionEvent:
        from infrastructure.events.interaction import LogInteractionQueueEvent
        return LogInteractionQueueEvent()
