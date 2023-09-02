""" serie repository module """

from typing import Callable, Iterator
from contextlib import AbstractContextManager
from sqlalchemy.orm import Session
from app.models.serie_model import Serie
from app.schemas.serie_schema import SerieUpdate
from app.models.instance_model import Instance


class SerieRepo:
    """ serie repository class """

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    async def create(self, item: Serie) -> Serie:
        """ save serie """

        with self.session_factory() as session:
            session.add(item)
            session.commit()
            session.refresh(item)

        return item

    async def update(self, item: Serie, updates: SerieUpdate) -> Serie:
        """ update serie """

        with self.session_factory() as session:
            update_data = updates.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(item, key, value)

            session.add(item)
            session.commit()
            session.refresh(item)

        return item

    def fetch_all(self, skip: int = 0, limit: int = 100) -> Iterator[Serie]:
        """ get all series """

        with self.session_factory() as session:
            return session.query(Serie).offset(skip).limit(limit).all()

    def fetch_by_id(self, serie_id) -> Serie:
        """ get serie by id """

        with self.session_factory() as session:
            return session.query(Serie).filter(
                Serie.instanceUID == serie_id).first()

    def fetch_serie_instances(self, serie_id) -> Iterator[Serie]:
        """ get serie instances """

        with self.session_factory() as session:
            return session.query(Instance).filter(Instance.seriesID == serie_id).all()
