from typing import List

from domain.entities.metric import MetricEntity
from domain.repositories.metric import MetricRepository
from domain.exceptions import NotFound
from infrastructure.repositories.clients.sqlite.base import Session
from infrastructure.repositories.clients.sqlite.models.metric import Metric


class MetricSQLiteRepository(MetricRepository):
    def get_all(self) -> List[MetricEntity]:
        with Session() as session:
            metrics = session.query(Metric).all()
            return [metric.to_entity() for metric in metrics]

    def get(self, metric_id: str) -> MetricEntity:
        with Session() as session:
            metric = session.query(Metric).filter(Metric.id == metric_id).first()
            if not metric:
                raise NotFound(f'Metric with id {metric_id}')
            return metric.to_entity()

    def filter_by(self, interaction_id: int = None) -> List[MetricEntity]:
        with Session() as session:
            query = session.query(Metric)
            if interaction_id:
                query = query.filter(Metric.interaction_id == interaction_id)
            metrics = query.all()
            return [metric.to_entity() for metric in metrics]

    def create(self, metric: MetricEntity) -> MetricEntity:
        with Session() as session:
            metric_model = Metric(
                id=metric.id,
                metric_name=metric.metric_name,
                interaction_id=metric.interaction_id,
                input_metric_value=metric.input_value,
                output_metric_value=metric.output_value
            )
            session.add(metric_model)
            session.commit()
            return metric_model.to_entity()

    def batch_create(self, metrics: List[MetricEntity]) -> List[MetricEntity]:
        if not metrics:
            return []
            
        with Session() as session:
            metric_models = [
                Metric(
                    id=metric.id,
                    metric_name=metric.metric_name,
                    interaction_id=metric.interaction_id,
                    input_metric_value=metric.input_value,
                    output_metric_value=metric.output_value
                ) for metric in metrics
            ]
            session.add_all(metric_models)
            session.commit()
            return [metric.to_entity() for metric in metric_models]

    def update(self, metric: MetricEntity) -> MetricEntity:
        with Session() as session:
            metric_model = session.query(Metric).filter(Metric.id == metric.id).first()
            if not metric_model:
                raise NotFound(f'Metric with id {metric.id}')
            metric_model.metric_type = metric.metric_type
            metric_model.interaction_id = metric.interaction

    def delete(self, metric_id: str) -> MetricEntity:
        with Session() as session:
            metric = session.query(Metric).filter(Metric.id == metric_id).first()
            if not metric:
                raise NotFound(f'Metric with id {metric_id}')
            session.delete(metric)
            session.commit()
            return metric.to_entity()
