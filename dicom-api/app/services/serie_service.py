""" serie service module """

from typing import Iterator
from app.repositories.serie_repository import SerieRepo
from app.models.serie_model import Serie
from app.schemas.serie_schema import SerieCreate, SerieUpdate
from app.errors import NotFoundException


class SerieService:
    """ serie service class """

    def __init__(self, serie_repository: SerieRepo) -> None:
        self._repository: SerieRepo = serie_repository

    def create(self, item: SerieCreate) -> Serie:
        """ save serie """

        serie = Serie(instanceUID=item.instanceUID, studyID=item.studyID,
                      filepath=item.filepath, description=item.description,
                      dimX=item.dimX, dimY=item.dimY, dimZ=item.dimZ,
                      pixelSpacing=item.pixelSpacing,
                      scaleX=item.scaleX, scaleY=item.scaleY, scaleZ=item.scaleZ)
        return self._repository.create(serie)

    def update(self, item: SerieUpdate, serie_id) -> Serie:
        """ update serie """

        serie = self.fetch_by_id(serie_id)
        serie.bitspath = item.bitspath

        return self._repository.update(serie, item)

    def fetch_all(self) -> Iterator[Serie]:
        """ get all series"""

        return self._repository.fetch_all()

    def fetch_by_id(self, serie_id) -> Serie:
        """ get serie by id """

        serie = self._repository.fetch_by_id(serie_id)
        if not serie:
            raise NotFoundException("There is no serie with the given id")
        return serie

    def fetch_serie_instances(self, serie_id) -> Iterator[Serie]:
        """ get serie instances """

        serie = self.fetch_by_id(serie_id)
        return self._repository.fetch_serie_instances(serie.id)
