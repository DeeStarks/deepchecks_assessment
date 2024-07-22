from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from typing import List

from application.services.alert import AlertService
from domain.entities.alert import AlertType
from domain.entities.interaction import InteractionType
from infrastructure.container import Container
from infrastructure.handlers.schemas.alert import AlertOutput


router = APIRouter(
    prefix='/alerts',
    tags=['alerts']
)


@router.get('/', response_model=List[AlertOutput])
@inject
def get_alerts(
    interaction_id: int = None,
    interaction_type: InteractionType = None,
    alert_type: AlertType = None,
    alert_service: AlertService = Depends(Provide[Container.alert_service])
) -> List[dict]:
    return [alert.to_dict() for alert in alert_service.filter_alerts(
        interaction_id=interaction_id,
        interaction_type=interaction_type,
        alert_type=alert_type
    )]
