""" patient service tests module """

import pytest
from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from app.services.patient_service import PatientService
from containers import Container
from app.errors import NotFoundException


@inject
async def test_fetch_by_id_should_throw_not_found_when_invalid_id_is_provider(
        patient_service: PatientService = Depends(Provide[Container.services.patient_service])):
    """ fetch by id test  """

    try:
        patient_service.fetch_by_id("123123.123123.123")
        pytest.fail("should throw an exception")
    except NotFoundException as err:
        assert err.status_code == 404


@inject
async def test_fetch_patient_studies_should_throw_not_found_when_invalid_id_is_provided(
        patient_service: PatientService =
        Depends(Provide[Container.services.patient_service])):
    """ fetch patient studies test  """

    try:
        patient_service.fetch_patient_studies("123123.123123.123")
        pytest.fail("should throw an exception")
    except NotFoundException as err:
        assert err.status_code == 404
