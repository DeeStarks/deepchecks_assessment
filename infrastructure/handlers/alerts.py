from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from application.services.alert import AlertService
from domain.entities.alert import AlertType
from domain.entities.interaction import InteractionType
from infrastructure.container import Container
from infrastructure.handlers.schemas.alert import AlertOutput

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("/", response_model=List[AlertOutput])
@inject
def get_alerts(
    page_number: int = 1,
    page_size: int = 30,
    interaction_id: int = None,
    interaction_type: InteractionType = None,
    alert_type: AlertType = None,
    alert_service: AlertService = Depends(Provide[Container.alert_service]),
) -> List[dict]:
    return [
        alert.to_dict()
        for alert in alert_service.filter_alerts(
            interaction_id=interaction_id,
            interaction_type=interaction_type,
            alert_type=alert_type,
            page_number=page_number,
            page_size=page_size,
        )
    ]


@router.get("/{alert_id}", response_model=AlertOutput)
@inject
def get_alert(
    alert_id: str,
    alert_service: AlertService = Depends(Provide[Container.alert_service]),
) -> dict:
    return alert_service.get_alert(alert_id).to_dict()
