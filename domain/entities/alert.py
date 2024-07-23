import uuid
from datetime import datetime
from enum import Enum


class AlertType(str, Enum):
    THRESHOLD = "threshold"
    OUTLIER = "outlier"


class AlertEntity:
    def __init__(
        self,
        alert_id: str,
        alert_type: str,
        interaction_id: str,
        interaction_type: str,
        value: float,
        created_at: datetime = None,
    ):
        self.id = alert_id
        self.alert_type = alert_type
        self.interaction_id = interaction_id
        self.interaction_type = interaction_type
        self.value = value
        self.created_at = created_at

    def to_dict(self):
        return {
            "alert_id": self.id,
            "alert_type": self.alert_type,
            "interaction_id": self.interaction_id,
            "interaction_type": self.interaction_type,
            "value": self.value,
            "created_at": self.created_at,
        }


class AlertFactory:
    @staticmethod
    def create(
        alert_type: str, interaction_id: str, interaction_type: str, value: float
    ) -> AlertEntity:
        return AlertEntity(
            alert_id=uuid.uuid4().__str__(),
            alert_type=alert_type,
            interaction_id=interaction_id,
            interaction_type=interaction_type,
            value=value,
        )
