from datetime import datetime
from pydantic import BaseModel


class MetricInput(BaseModel):
    metric_name: str
    interaction_id: str
    input_value: float
    output_value: float


class MetricOutput(BaseModel):
    metric_id: str
    metric_name: str
    interaction_id: str
    input_value: float
    output_value: float
    created_at: datetime
