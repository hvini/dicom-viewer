""" patient routers module """

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.services.patient_service import PatientService
from app.errors import NotFoundException
from containers import Container

router = APIRouter(
    prefix='/patients',
    tags=['Patients']
)


@router.get('/')
@inject
def get_patients(patient_service: PatientService =
                 Depends(Provide[Container.services.patient_service])):
    """ get all patients """

    patients = patient_service.fetch_all()
    return JSONResponse(
        content={
            "status": "success",
            "data": jsonable_encoder(patients)
        }
    )


@router.get('/{patient_id}/studies')
@inject
def get_patient_studies(patient_id: str, patient_service: PatientService =
                        Depends(Provide[Container.services.patient_service])):
    """ get patient studies """

    try:
        studies = patient_service.fetch_patient_studies(patient_id)
        return JSONResponse(
            content={
                "status": "success",
                "data": jsonable_encoder(studies)
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
