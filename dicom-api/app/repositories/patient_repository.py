""" patient repository module """

from typing import Callable, Iterator
from contextlib import AbstractContextManager
from sqlalchemy.orm import Session
from app.models.patient_model import Patient
from app.models.study_model import Study


class PatientRepo:
    """ patient repository class """

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    async def create(self, item: Patient) -> Patient:
        """ save patient """

        with self.session_factory() as session:
            session.add(item)
            session.commit()
            session.refresh(item)

        return item

    def fetch_all(self, skip: int = 0, limit: int = 100) -> Iterator[Patient]:
        """ get all patients """

        with self.session_factory() as session:
            return session.query(Patient).offset(skip).limit(limit).all()

    def fetch_by_id(self, patient_id) -> Patient:
        """ get a patient by id """

        with self.session_factory() as session:
            return session.query(Patient).filter(
                Patient.patientID == patient_id).first()

    def fetch_patient_studies(self, patient_id) -> Iterator[Patient]:
        """ get patient studies """

        with self.session_factory() as session:
            return session.query(Study).filter(Study.patientID == patient_id).all()
