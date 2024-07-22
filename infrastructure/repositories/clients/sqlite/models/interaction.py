from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from domain.entities.interaction import InteractionEntity
from infrastructure.repositories.clients.sqlite.models import Base


class Interaction(Base):
    __tablename__ = 'interactions'
    id = Column(String, primary_key=True)
    input_text = Column(String, nullable=False)
    output_text = Column(String, nullable=False)
    metrics = relationship('Metric', back_populates='interaction')
    alerts = relationship('Alert', back_populates='interaction')

    def to_entity(self) -> InteractionEntity:
        return InteractionEntity(
            interaction_id=self.id,
            input_text=self.input_text,
            output_text=self.output_text
        )
