""" study service module """

from typing import Iterator
from app.repositories.study_repository import StudyRepo
from app.models.study_model import Study
from app.schemas.study_schema import StudyCreate
from app.errors import NotFoundException


class StudyService:
    """ study service class """

    def __init__(self, study_repository: StudyRepo) -> None:
        self._repository: StudyRepo = study_repository

    def create(self, item: StudyCreate) -> Study:
        """ save study """

        study = Study(instanceUID=item.instanceUID, patientID=item.patientID,
                      description=item.description, time=item.time)
        return self._repository.create(study)

    def fetch_all(self) -> Iterator[Study]:
        """ get all studies """

        return self._repository.fetch_all()

    def fetch_by_id(self, study_id) -> Study:
        """ get study by id """

        study = self._repository.fetch_by_id(study_id)
        if not study:
            raise NotFoundException("There is no study with the given id")
        return study

    def fetch_study_series(self, study_id):
        """ get study series """

        study = self.fetch_by_id(study_id)
        return self._repository.fetch_study_series(study.id)
