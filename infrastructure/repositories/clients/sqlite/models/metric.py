from sqlalchemy import Column, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from domain.entities.metric import MetricEntity
from infrastructure.repositories.clients.sqlite.models import Base


class Metric(Base):
    __tablename__ = "metrics"
    id = Column(String, primary_key=True)
    interaction_id = Column(String, ForeignKey("interactions.id"), nullable=False)
    metric_name = Column(String, nullable=False)
    input_metric_value = Column(Float, nullable=False)
    output_metric_value = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    interaction = relationship("Interaction", back_populates="metrics")

    def to_entity(self) -> MetricEntity:
        return MetricEntity(
            metric_id=self.id,
            metric_name=self.metric_name,
            interaction_id=self.interaction_id,
            input_value=self.input_metric_value,
            output_value=self.output_metric_value,
            created_at=self.created_at,
        )
