""" instance service module """

from typing import Iterator
from app.repositories.instance_repository import InstanceRepo
from app.services.serie_service import SerieService
from app.models.instance_model import Instance
from app.schemas.instance_schema import InstanceCreate


class InstanceService:
    """ instance service class """

    def __init__(self, instance_repository: InstanceRepo, serie_service: SerieService) -> None:
        self._repository: InstanceRepo = instance_repository
        self._serie_service: SerieService = serie_service

    def create(self, item: InstanceCreate) -> Instance:
        """ save instance """

        instance = Instance(seriesID=item.seriesID, filename=item.filename)
        return self._repository.create(instance)

    def fetch_all(self) -> Iterator[Instance]:
        """ get all instances """

        return self._repository.fetch_all()

    def delete_by_serie_id(self, serie_id) -> None:
        """ delete instance by serie id """

        serie = self._serie_service.fetch_by_id(serie_id)
        return self._repository.delete_by_serie_id(serie.id)
