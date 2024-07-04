class MetricCalculator:
    """Base class for metric calculators.
    """
    def calculate(self, text):
        raise NotImplementedError


class LengthMetric(MetricCalculator):
    """A subclass of MetricCalculator that calculates the length of a string.
    """
    def calculate(self, text):
        return len(text)


length_metric_calculator = LengthMetric()
