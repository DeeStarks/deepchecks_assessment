from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from domain.entities.metric import MetricEntity
from infrastructure.repositories.clients.sqlite.models import Base


class Metric(Base):
    __tablename__ = 'metrics'
    id = Column(String, primary_key=True)
    interaction_id = Column(String, ForeignKey('interactions.id'), nullable=False)
    metric_name = Column(String, nullable=False)
    input_metric_value = Column(Float, nullable=False)
    output_metric_value = Column(Float, nullable=False)
    interaction = relationship('Interaction', back_populates='metrics')

    def to_entity(self) -> MetricEntity:
        return MetricEntity(
            metric_id=self.id,
            metric_name=self.metric_name,
            interaction_id=self.interaction_id,
            input_value=self.input_metric_value,
            output_value=self.output_metric_value
        )
