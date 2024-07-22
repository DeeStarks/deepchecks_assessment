from abc import ABC, abstractmethod
from typing import List

from domain.entities.alert import AlertEntity


class AlertRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[AlertEntity]:
        raise NotImplementedError

    @abstractmethod
    def get(self, alert_id: str) -> AlertEntity:
        raise NotImplementedError

    @abstractmethod
    def filter_by(
        self,
        interaction_id: int = None,
        interaction_type: str = None,
        alert_type: str = None
    ) -> List[AlertEntity]:
        raise NotImplementedError

    @abstractmethod
    def create(self, alert: AlertEntity) -> AlertEntity:
        raise NotImplementedError

    @abstractmethod
    def batch_create(self, alerts: List[AlertEntity]) -> List[AlertEntity]:
        raise NotImplementedError

    @abstractmethod
    def update(self, alert: AlertEntity) -> AlertEntity:
        raise NotImplementedError

    @abstractmethod
    def delete(self, alert_id: str) -> AlertEntity:
        raise NotImplementedError
