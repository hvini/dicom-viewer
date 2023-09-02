""" study repository module """

from typing import Callable, Iterator
from contextlib import AbstractContextManager
from sqlalchemy.orm import Session
from app.models.study_model import Study
from app.models.serie_model import Serie


class StudyRepo:
    """ patient repository class """

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    async def create(self, item: Study) -> Study:
        """ save study """

        with self.session_factory() as session:
            session.add(item)
            session.commit()
            session.refresh(item)

        return item

    def fetch_all(self, skip: int = 0, limit: int = 100) -> Iterator[Study]:
        """ get all studies """

        with self.session_factory() as session:
            return session.query(Study).offset(skip).limit(limit).all()

    def fetch_by_id(self, study_id) -> Study:
        """ get study by id """

        with self.session_factory() as session:
            return session.query(Study).filter(
                Study.instanceUID == study_id).first()

    def fetch_study_series(self, study_id) -> Iterator[Study]:
        """ get study series """

        with self.session_factory() as session:
            return session.query(Serie).filter(Serie.studyID == study_id).all()
