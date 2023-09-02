""" database module """

import os
from contextlib import contextmanager, AbstractContextManager
from typing import Callable
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, orm

Base = declarative_base()


class Database:
    """ database class """

    # def __init__(self, db_url: str) -> None:
    def __init__(self) -> None:

        db_url = os.environ.get("DB_URL")
        self._engine = create_engine(db_url, echo=True)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine
            )
        )

    def create_database(self) -> None:
        """ create tables """

        Base.metadata.create_all(self._engine)

    def drop_database(self) -> None:
        """ drop tables """

        Base.metadata.drop_all(self._engine)

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        """ session """

        session: Session = self._session_factory()

        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
