""" serie routers module """

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.services.serie_service import SerieService
from app.schemas.serie_schema import SerieUpdate, Serie
from app.errors import NotFoundException
from containers import Container

router = APIRouter(
    prefix='/series',
    tags=['Series']
)


@router.get('/')
@inject
def get_series(serie_service: SerieService = Depends(Provide[Container.services.serie_service])):
    """ get all series"""

    series = serie_service.fetch_all()
    return JSONResponse(
        content={
            "status": "success",
            "data": jsonable_encoder(series)
        }
    )


@router.put('/{serie_id}/update', response_model=Serie)
@inject
async def update_serie(item: SerieUpdate, serie_id: str, serie_service: SerieService =
                       Depends(Provide[Container.services.serie_service])):
    """ update serie """

    try:
        serie = await serie_service.update(item, serie_id)
        return JSONResponse(
            content={
                "status": "success",
                "data": jsonable_encoder(serie)
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


@router.get('/{serie_id}/instances')
@inject
def get_serie_instances(serie_id: str, serie_service: SerieService =
                        Depends(Provide[Container.services.serie_service])):
    """ get serie instances """

    try:
        instances = serie_service.fetch_serie_instances(serie_id)
        return JSONResponse(
            content={
                "status": "success",
                "data": jsonable_encoder(instances)
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
