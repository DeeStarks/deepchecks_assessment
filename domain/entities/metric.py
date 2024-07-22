import uuid


class MetricEntity:
    def __init__(
        self,
        metric_id: str,
        metric_name: str,
        interaction_id: str,
        input_value: float,
        output_value: float
    ):
        self.id = metric_id
        self.metric_name = metric_name
        self.interaction_id = interaction_id
        self.input_value = input_value
        self.output_value = output_value

    def to_dict(self):
        return {
            'metric_id': self.id,
            'metric_name': self.metric_name,
            'interaction_id': self.interaction_id,
            'input_value': self.input_value,
            'output_value': self.output_value
        }


class MetricFactory:
    @staticmethod
    def create(
        metric_name: str,
        interaction_id: str,
        input_value: float,
        output_value: float,
    ) -> MetricEntity:
        return MetricEntity(
            metric_id=uuid.uuid4().__str__(),
            metric_name=metric_name,
            interaction_id=interaction_id,
            input_value=input_value,
            output_value=output_value
        )
