from domain.entities.metric import MetricEntity
from domain.repositories.metric import MetricRepository
from domain.usecases.metric import MetricCalculatorUsecase, MetricUsecase


class MetricService(MetricUsecase):
    def __init__(self, repository: MetricRepository):
        super().__init__(repository)

    def all_metrics(self, page_number: int, page_size: int) -> list[MetricEntity]:
        return self.repository.get_all(page_number, page_size)

    def filter_metrics(
        self, interaction_id: int, page_number: int, page_size: int
    ) -> list[MetricEntity]:
        return self.repository.filter_by(
            interaction_id=interaction_id, page_number=page_number, page_size=page_size
        )

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


class LengthMetricCalculator(MetricCalculatorUsecase):
    def calculate(self, text: str) -> float:
        return len(text)
