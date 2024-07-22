import os
import uuid

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, UploadFile
from typing import List, Dict

from application.services.interaction import InteractionService
from config.config import BASE_DIR
from infrastructure.container import Container
from infrastructure.handlers.schemas.interaction import InteractionOutput


router = APIRouter(
    prefix='/interactions',
    tags=['interactions']
)


@router.get('/', response_model=List[InteractionOutput])
@inject
def get_interactions(
    interaction_service: InteractionService = Depends(Provide[Container.interaction_service])
) -> List[dict]:
    return [interaction.to_dict() for interaction in interaction_service.all_interactions()]


@router.post('-csv', response_model=Dict[str, str])
@inject
def log_interaction_from_csv(
    file: UploadFile,
    interaction_service: InteractionService = Depends(Provide[Container.interaction_service])
) -> Dict[str, str]:
    # saving the uploaded file to a temporary location so that we can read it in the event handler
    if not (BASE_DIR / "tmp").exists():
        (BASE_DIR / "tmp").mkdir()

    filename = BASE_DIR / "tmp" / f"{uuid.uuid4()}.csv"
    with open(filename, "wb") as f:
        f.write(file.file.read())

    interaction_service.create_interactions_from_file(filename.as_posix())
    return {"message": "Uploaded interactions are being logged"}
