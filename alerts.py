from models import InteractionType


class Alert:
    """Base class for alerts. Alerts are used to notify users when certain conditions are met.
    """
    def check(self, metric_value):
        raise NotImplementedError


class ThresholdAlert(Alert):
    """A subclass of Alert that notifies users when a metric value exceeds a threshold.
    """
    def __init__(self, high: float, low: float):
        self.high = high
        self.low = low

    def check(self, metric_value):
        return (metric_value > self.high) or (metric_value < self.low)


class OutlierAlert(Alert):
    """A subclass of Alert that notifies users when a metric value is an outlier
    based on a list of values.
    """
    def __init__(self, input_values: list[float], output_values: list[float]):
        self.input_values = input_values
        self.output_values = output_values

    def check(self, metric_value: float, interaction_type: str):
        """
        Check if the metric value is an outlier based on the list of values.
        
        The metric value is considered an outlier if it is more than or less than
        2 standard deviations away from the mean of the values.
        """
        if interaction_type == InteractionType.INPUT:
            values = self.input_values
        elif interaction_type == InteractionType.OUTPUT:
            values = self.output_values
        else:
            raise ValueError("Invalid interaction type")

        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std_dev = variance ** 0.5
        return (metric_value > mean + 2 * std_dev) or (metric_value < mean - 2 * std_dev)


threshold_alert = ThresholdAlert(
    high=100,
    low=10
)
outlier_alert = OutlierAlert(
    input_values=[],
    output_values=[]
)
