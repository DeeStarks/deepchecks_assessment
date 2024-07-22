import uuid

from enum import Enum


class AlertType(str, Enum):
    THRESHOLD = 'threshold'
    OUTLIER = 'outlier'


class AlertEntity:
    def __init__(
        self,
        alert_id: str,
        alert_type: str,
        interaction_id: str,
        interaction_type: str,
        value: float
    ):
        self.id = alert_id
        self.alert_type = alert_type
        self.interaction_id = interaction_id
        self.interaction_type = interaction_type
        self.value = value

    def to_dict(self):
        return {
            'alert_id': self.id,
            'alert_type': self.alert_type,
            'interaction_id': self.interaction_id,
            'interaction_type': self.interaction_type,
            'value': self.value
        }


class AlertFactory:
    @staticmethod
    def create(
        alert_type: str,
        interaction_id: str,
        interaction_type: str,
        value: float
    ) -> AlertEntity:
        return AlertEntity(
            alert_id=uuid.uuid4().__str__(),
            alert_type=alert_type,
            interaction_id=interaction_id,
            interaction_type=interaction_type,
            value=value
        )
