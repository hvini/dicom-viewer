""" api routers module """

from fastapi import APIRouter
from app.api.endpoints import (
    patient_routers, study_routers, serie_routers, instance_routers, dicom_routers)

router = APIRouter()

router.include_router(patient_routers.router)
router.include_router(study_routers.router)
router.include_router(serie_routers.router)
router.include_router(instance_routers.router)
router.include_router(dicom_routers.router)
