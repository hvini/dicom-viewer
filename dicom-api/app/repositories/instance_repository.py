""" instance repository module """

from typing import Callable, Iterator
from contextlib import AbstractContextManager
from sqlalchemy.orm import Session
from app.models.instance_model import Instance


class InstanceRepo:
    """ instance repository class """

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    async def create(self, item: Instance) -> Instance:
        """ save instance """

        with self.session_factory() as session:
            session.add(item)
            session.commit()
            session.refresh(item)

        return item

    def fetch_all(self, skip: int = 0, limit: int = 100) -> Iterator[Instance]:
        """ get all instances """

        with self.session_factory() as session:
            return session.query(Instance).offset(skip).limit(limit).all()

    def delete_by_serie_id(self, serie_id) -> None:
        """ delete instance by serie id """

        with self.session_factory() as session:
            session.query(Instance).filter(
                Instance.seriesID == serie_id).delete()
