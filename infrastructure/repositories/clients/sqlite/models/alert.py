from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from domain.entities.alert import AlertEntity
from infrastructure.repositories.clients.sqlite.models import Base


class Alert(Base):
    __tablename__ = 'alerts'
    id = Column(String, primary_key=True)
    alert_type = Column(String, nullable=False)
    interaction_id = Column(String, ForeignKey('interactions.id'), nullable=False)
    interaction_type = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    interaction = relationship('Interaction', back_populates='alerts')

    def to_entity(self) -> AlertEntity:
        return AlertEntity(
            alert_id=self.id,
            alert_type=self.alert_type,
            interaction_id=self.interaction_id,
            interaction_type=self.interaction_type,
            value=self.value
        )
