from abc import ABC, abstractmethod

from domain.events.runners.detached import DetachedRunner


class LogInteractionEvent(ABC):
    @abstractmethod
    def send(self, runner: DetachedRunner, filename: str) -> bool:
        raise NotImplementedError
