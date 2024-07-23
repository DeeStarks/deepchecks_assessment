from abc import ABC, abstractmethod
from typing import List

from domain.entities.interaction import InteractionEntity
from domain.events.interaction import LogInteractionEvent
from domain.events.runners.detached import DetachedRunner
from domain.repositories.interaction import InteractionRepository


class InteractionUsecase(ABC):
    @abstractmethod
    def __init__(
        self,
        repository: InteractionRepository,
        event: LogInteractionEvent,
        event_runner: DetachedRunner
    ):
        self.repository = repository
        self.event = event
        self.event_runner = event_runner

    @abstractmethod
    def all_interactions(self, page_number: int, page_size: int) -> List[InteractionEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_interaction(self, interaction_id: str) -> InteractionEntity:
        raise NotImplementedError

    @abstractmethod
    def create_interaction(self, interaction: InteractionEntity) -> InteractionEntity:
        raise NotImplementedError

    @abstractmethod
    def batch_create_interactions(self, interactions: List[InteractionEntity]) -> List[InteractionEntity]:
        raise NotImplementedError

    @abstractmethod
    def create_interactions_from_file(self, file_path: str) -> List[InteractionEntity]:
        raise NotImplementedError

    @abstractmethod
    def update_interaction(self, interaction: InteractionEntity) -> InteractionEntity:
        raise NotImplementedError

    @abstractmethod
    def delete_interaction(self, interaction_id: str) -> InteractionEntity:
        raise NotImplementedError
