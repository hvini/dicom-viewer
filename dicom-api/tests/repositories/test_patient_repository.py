""" patient repository tests module """

from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from app.repositories.patient_repository import PatientRepo
from containers import Container
from app.models.patient_model import Patient


@inject
async def test_fetch_all_should_return_an_empty_list_when_table_is_empty(
        patient_repository: PatientRepo =
        Depends(Provide[Container.repositories.patient_repository])):
    """ fetch all patients test """

    patients = patient_repository.fetch_all()

    assert patients is not None
    assert len(patients) == 0


@inject
async def test_fetch_by_id_should_return_none_when_invalid_id_is_provided(
        patient_repository: PatientRepo =
        Depends(Provide[Container.repositories.patient_repository])):
    """ fetch by id test """

    patient = patient_repository.fetch_by_id(1)
    assert patient is None


@inject
async def test_create_should_return_inserted_data_when_valid_data_is_provided(
        patient_repository: PatientRepo =
        Depends(Provide[Container.repositories.patient_repository])):
    """ save test """

    item = Patient(
        patientID="1231232.12323.321",
        name="vinícius",
        birthDate="1672510442"
    )
    patient = await patient_repository.create(item)
    assert patient == item


@inject
async def test_fetch_patient_studies_should_return_empty_list_when_invalid_id_is_provided(
        patient_repository: PatientRepo =
        Depends(Provide[Container.repositories.patient_repository])):
    """ fetch patient studies test """

    studies = patient_repository.fetch_patient_studies(1)
    assert len(studies) == 0
