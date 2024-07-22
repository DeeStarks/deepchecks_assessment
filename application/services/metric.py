from domain.entities.metric import MetricEntity
from domain.repositories.metric import MetricRepository
from domain.usecases.metric import MetricUsecase


class MetricService(MetricUsecase):
    def __init__(self, repository: MetricRepository):
        super().__init__(repository)

    def all_metrics(self) -> list[MetricEntity]:
        return self.repository.get_all()

    def filter_metrics(self, interaction_id: int = None) -> list[MetricEntity]:
        return self.repository.filter_by(interaction_id=interaction_id)

    def get_metric(self, metric_id: str) -> MetricEntity:
        return self.repository.get(metric_id)

    def create_metric(self, metric: MetricEntity) -> MetricEntity:
        return self.repository.create(metric)

    def batch_create_metrics(self, metrics: list[MetricEntity]) -> list[MetricEntity]:
        return self.repository.batch_create(metrics)

    def update_metric(self, metric: MetricEntity) -> MetricEntity:
        return self.repository.update(metric)

    def delete_metric(self, metric_id: str) -> MetricEntity:
        return self.repository.delete(metric_id)


class _BaseMetricCalculator:
    """Base class for metric calculators."""
    def calculate(self, text: str) -> float:
        raise NotImplementedError


class LengthMetricCalculator(_BaseMetricCalculator):
    """A subclass of MetricCalculator that calculates the length of a string."""
    def calculate(self, text: str) -> float:
        return len(text)
