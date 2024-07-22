from domain.entities.alert import AlertEntity
from domain.entities.interaction import InteractionType
from domain.exceptions import InvalidInteractionType
from domain.repositories.alert import AlertRepository
from domain.usecases.alert import AlertUsecase


class AlertService(AlertUsecase):
    def __init__(self, repository: AlertRepository):
        super().__init__(repository)

    def all_alerts(self) -> list[AlertEntity]:
        return self.repository.get_all()

    def filter_alerts(
        self,
        interaction_id: int = None,
        interaction_type: str = None,
        alert_type: str = None
    ) -> list[AlertEntity]:
        return self.repository.filter_by(
            interaction_id=interaction_id,
            interaction_type=interaction_type,
            alert_type=alert_type
        )

    def get_alert(self, alert_id: str) -> AlertEntity:
        return self.repository.get(alert_id)

    def create_alert(self, alert: AlertEntity) -> AlertEntity:
        return self.repository.create(alert)

    def batch_create_alerts(self, alerts: list[AlertEntity]) -> list[AlertEntity]:
        return self.repository.batch_create(alerts)

    def update_alert(self, alert: AlertEntity) -> AlertEntity:
        return self.repository.update(alert)

    def delete_alert(self, alert_id: str) -> AlertEntity:
        return self.repository.delete(alert_id)


class _BaseAlertChecker:
    """Base alert checker class"""
    def check(self, value: float) -> bool:
        raise NotImplementedError


class ThresholdAlertChecker(_BaseAlertChecker):
    """A subclass of AlertChecker that notifies when a metric value exceeds a threshold."""
    def __init__(self, high: float, low: float):
        self.high = high
        self.low = low

    def get_thresholds(self) -> tuple[float, float]:
        return self.high, self.low

    def check(self, value: float) -> bool:
        return (value > self.high) or (value < self.low)


class OutlierAlertChecker(_BaseAlertChecker):
    """A subclass of AlertChecker that notifies when a metric value is an outlier."""
    def __init__(self, prev_inputs: list[float] = [], prev_outputs: list[float] = []):
        self.prev_inputs = prev_inputs
        self.prev_outputs = prev_outputs

    def check(self, value: float, interaction_type: str) -> bool:
        """
        Check if the metric value is an outlier based on the list of values.

        The metric value is considered an outlier if it is more than or less than
        2 standard deviations away from the mean of the values.
        """
        values = []
        
        if interaction_type == InteractionType.INPUT:
            values = self.prev_inputs
        elif interaction_type == InteractionType.OUTPUT:
            values = self.prev_outputs
        else:
            raise InvalidInteractionType(interaction_type)

        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std_dev = variance ** 0.5
        return (value > mean + 2 * std_dev) or (value < mean - 2 * std_dev)
