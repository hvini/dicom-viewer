""" patient service module """

from typing import Iterator
from app.repositories.patient_repository import PatientRepo
from app.models.patient_model import Patient
from app.schemas.patient_schema import PatientCreate
from app.errors import NotFoundException


class PatientService:
    """ patients service class """

    def __init__(self, patient_repository: PatientRepo) -> None:
        self._repository: PatientRepo = patient_repository

    def create(self, item: PatientCreate) -> Patient:
        """ save patient """

        patient = Patient(patientID=item.patientID,
                          name=item.name, birthDate=item.birthDate)
        return self._repository.create(patient)

    def fetch_all(self) -> Iterator[Patient]:
        """ get all patients """

        return self._repository.fetch_all()

    def fetch_by_id(self, patient_id) -> Patient:
        """ get patient by id  """

        patient = self._repository.fetch_by_id(patient_id)
        if not patient:
            raise NotFoundException(
                "There is no patient with the given id")
        return patient

    def fetch_patient_studies(self, patient_id) -> Patient:
        """ get patient studies """

        patient = self.fetch_by_id(patient_id)
        return self._repository.fetch_patient_studies(patient.id)
