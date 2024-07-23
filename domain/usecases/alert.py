from abc import ABC, abstractmethod
from typing import List

from domain.entities.alert import AlertEntity
from domain.repositories.alert import AlertRepository


class AlertUsecase(ABC):
    @abstractmethod
    def __init__(self, repository: AlertRepository):
        self.repository = repository

    @abstractmethod
    def all_alerts(self, page_number: int, page_size: int) -> List[AlertEntity]:
        raise NotImplementedError

    @abstractmethod
    def filter_alerts(
        self,
        interaction_id: int,
        interaction_type: str,
        alert_type: str,
        page_number: int,
        page_size: int,
    ) -> List[AlertEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_alert(self, alert_id: str) -> AlertEntity:
        raise NotImplementedError

    @abstractmethod
    def create_alert(self, alert: AlertEntity) -> AlertEntity:
        raise NotImplementedError

    @abstractmethod
    def batch_create_alerts(self, alerts: List[AlertEntity]) -> List[AlertEntity]:
        raise NotImplementedError

    @abstractmethod
    def update_alert(self, alert: AlertEntity) -> AlertEntity:
        raise NotImplementedError

    @abstractmethod
    def delete_alert(self, alert_id: str) -> AlertEntity:
        raise NotImplementedError


class AlertCheckerUsecase(ABC):
    @abstractmethod
    def check(self, value: float) -> bool:
        raise NotImplementedError
