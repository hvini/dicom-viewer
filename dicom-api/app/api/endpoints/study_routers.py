""" study routers module """

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.services.study_service import StudyService
from app.errors import NotFoundException
from containers import Container

router = APIRouter(
    prefix='/studies',
    tags=['Studies']
)


@router.get('/')
@inject
def get_studies(study_service: StudyService = Depends(Provide[Container.services.study_service])):
    """ get all studies """

    studies = study_service.fetch_all()
    return JSONResponse(
        content={
            "status": "success",
            "data": jsonable_encoder(studies)
        }
    )


@router.get('/{study_id}/series')
@inject
def get_study_series(study_id: str, study_service: StudyService =
                     Depends(Provide[Container.services.study_service])):
    """ get study series """

    try:
        series = study_service.fetch_study_series(study_id)
        return JSONResponse(
            content={
                "status": "success",
                "data": jsonable_encoder(series)
            }
        )
    except NotFoundException as err:
        return JSONResponse(
            status_code=err.status_code,
            content={
                "status": "error",
                "message": err.detail
            }
        )
