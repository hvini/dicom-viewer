""" instance routers module """

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.services.instance_service import InstanceService
from containers import Container

router = APIRouter(
    prefix='/instances',
    tags=['Instances']
)


@router.get('/')
@inject
def get_instances(instance_service: InstanceService =
                  Depends(Provide[Container.services.instance_service])):
    """ get all instances """

    instances = instance_service.fetch_all()
    return JSONResponse(
        content={
            "status": "success",
            "data": jsonable_encoder(instances)
        }
    )
