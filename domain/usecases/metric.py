from abc import ABC, abstractmethod
from typing import List

from domain.entities.metric import MetricEntity
from domain.repositories.metric import MetricRepository


class MetricUsecase(ABC):
    @abstractmethod
    def __init__(self, repository: MetricRepository):
        self.repository = repository

    @abstractmethod
    def all_metrics(self, page_number: int, page_size: int) -> List[MetricEntity]:
        raise NotImplementedError

    @abstractmethod
    def filter_metrics(
        self, interaction_id: int, page_number: int, page_size: int
    ) -> List[MetricEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_metric(self, metric_id: str) -> MetricEntity:
        raise NotImplementedError

    @abstractmethod
    def create_metric(self, metric: MetricEntity) -> MetricEntity:
        raise NotImplementedError

    @abstractmethod
    def batch_create_metrics(self, metrics: List[MetricEntity]) -> List[MetricEntity]:
        raise NotImplementedError

    @abstractmethod
    def update_metric(self, metric: MetricEntity) -> MetricEntity:
        raise NotImplementedError

    @abstractmethod
    def delete_metric(self, metric_id: str) -> MetricEntity:
        raise NotImplementedError


class MetricCalculatorUsecase(ABC):
    @abstractmethod
    def calculate(self, text: str) -> float:
        raise NotImplementedError
