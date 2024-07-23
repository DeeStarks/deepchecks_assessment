from datetime import datetime

from pydantic import BaseModel

from domain.entities.alert import AlertType
from domain.entities.interaction import InteractionType


class AlertInput(BaseModel):
    alert_type: AlertType
    interaction_id: str
    interaction_type: InteractionType
    value: float


class AlertOutput(BaseModel):
    alert_id: str
    alert_type: AlertType
    interaction_id: str
    interaction_type: InteractionType
    value: float
    created_at: datetime
