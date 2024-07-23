from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from domain.entities.interaction import InteractionEntity
from infrastructure.repositories.clients.sqlite.models import Base


class Interaction(Base):
    __tablename__ = 'interactions'
    id = Column(String, primary_key=True)
    input_text = Column(String, nullable=False)
    output_text = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    metrics = relationship('Metric', back_populates='interaction')
    alerts = relationship('Alert', back_populates='interaction')

    def to_entity(self) -> InteractionEntity:
        return InteractionEntity(
            interaction_id=self.id,
            input_text=self.input_text,
            output_text=self.output_text,
            created_at=self.created_at
        )
