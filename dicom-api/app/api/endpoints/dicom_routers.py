""" dicom routers module """

from typing import List
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide
from fastapi.encoders import jsonable_encoder
from app.services.dicom_service import DicomService
from containers import Container
from app.errors import NotFoundException

router = APIRouter(
    prefix='/dicoms',
    tags=['Dicoms']
)


@router.post('/upload')
@inject
async def upload_dicom(files: List[UploadFile] = File(...), dicom_service: DicomService =
                       Depends(Provide[Container.services.dicom_service])):
    """ upload dicom dir """

    await dicom_service.upload(files)
    return JSONResponse(
        status_code=201,
        content={
            "status": "success",
            "data": {"message": "Files successfully uploaded"}
        }
    )


@router.get('/gen_bits')
@inject
async def generate_bits(serie_id: str, dicom_service: DicomService =
                        Depends(Provide[Container.services.dicom_service])):
    """ generate .bits file """

    try:
        res = await dicom_service.generate_bits(serie_id)
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "data": jsonable_encoder(res)
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
