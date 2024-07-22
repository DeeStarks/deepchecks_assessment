from abc import ABC, abstractmethod
from typing import List

from domain.entities.interaction import InteractionEntity


class InteractionRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[InteractionEntity]:
        raise NotImplementedError

    @abstractmethod
    def get(self, interaction_id: str) -> InteractionEntity:
        raise NotImplementedError

    @abstractmethod
    def create(self, interaction: InteractionEntity) -> InteractionEntity:
        raise NotImplementedError

    @abstractmethod
    def batch_create(self, interactions: List[InteractionEntity]) -> List[InteractionEntity]:
        raise NotImplementedError

    @abstractmethod
    def update(self, interaction: InteractionEntity) -> InteractionEntity:
        raise NotImplementedError

    @abstractmethod
    def delete(self, interaction_id: str) -> InteractionEntity:
        raise NotImplementedError
