from abc import ABC, abstractmethod
from typing import List

from domain.entities.metric import MetricEntity


class MetricRepository(ABC):
    @abstractmethod
    def get_all(self, page_number: int = 1, page_size: int = 30) -> List[MetricEntity]:
        raise NotImplementedError

    @abstractmethod
    def get(self, metric_id: str) -> MetricEntity:
        raise NotImplementedError

    @abstractmethod
    def filter_by(
        self,
        interaction_id: int = None,
        page_number: int = 1,
        page_size: int = 30
    ) -> List[MetricEntity]:
        raise NotImplementedError

    @abstractmethod
    def create(self, metric: MetricEntity) -> MetricEntity:
        raise NotImplementedError

    @abstractmethod
    def batch_create(self, metrics: List[MetricEntity]) -> List[MetricEntity]:
        raise NotImplementedError

    @abstractmethod
    def update(self, metric: MetricEntity) -> MetricEntity:
        raise NotImplementedError

    @abstractmethod
    def delete(self, metric_id: str) -> MetricEntity:
        raise NotImplementedError
