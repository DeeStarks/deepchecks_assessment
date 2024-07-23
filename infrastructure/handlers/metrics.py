from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from typing import List

from application.services.metric import MetricService
from infrastructure.container import Container
from infrastructure.handlers.schemas.metric import MetricOutput


router = APIRouter(
    prefix='/metrics',
    tags=['metrics']
)


@router.get('/', response_model=List[MetricOutput])
@inject
def get_metrics(
    page_number: int = 1,
    page_size: int = 30,
    interaction_id: int = None,
    metric_service: MetricService = Depends(Provide[Container.metric_service])
) -> List[dict]:
    return [metric.to_dict() for metric in metric_service.filter_metrics(
        interaction_id=interaction_id,
        page_number=page_number,
        page_size=page_size
    )]


@router.get('/{metric_id}', response_model=MetricOutput)
@inject
def get_metric(
    metric_id: str,
    metric_service: MetricService = Depends(Provide[Container.metric_service])
) -> dict:
    return metric_service.get_metric(metric_id).to_dict()
