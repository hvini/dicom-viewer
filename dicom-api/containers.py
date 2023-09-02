""" container module """

from dependency_injector import containers, providers
from db import Database
from app.repositories.patient_repository import PatientRepo
from app.services.patient_service import PatientService
from app.repositories.study_repository import StudyRepo
from app.services.study_service import StudyService
from app.repositories.serie_repository import SerieRepo
from app.services.serie_service import SerieService
from app.repositories.instance_repository import InstanceRepo
from app.services.instance_service import InstanceService
from app.services.dicom_service import DicomService


class Gateways(containers.DeclarativeContainer):

    db = providers.Singleton(Database)


class Repositories(containers.DeclarativeContainer):

    gateways = providers.DependenciesContainer()

    patient_repository = providers.Factory(
        PatientRepo,
        session_factory=gateways.db.provided.session
    )

    study_repository = providers.Factory(
        StudyRepo,
        session_factory=gateways.db.provided.session
    )

    serie_repository = providers.Factory(
        SerieRepo,
        session_factory=gateways.db.provided.session
    )

    instance_repository = providers.Factory(
        InstanceRepo,
        session_factory=gateways.db.provided.session
    )


class Services(containers.DeclarativeContainer):

    repositories = providers.DependenciesContainer()

    patient_service = providers.Factory(
        PatientService,
        patient_repository=repositories.patient_repository
    )

    study_service = providers.Factory(
        StudyService,
        study_repository=repositories.study_repository
    )

    serie_service = providers.Factory(
        SerieService,
        serie_repository=repositories.serie_repository
    )

    instance_service = providers.Factory(
        InstanceService,
        instance_repository=repositories.instance_repository,
        serie_service=serie_service
    )

    dicom_service = providers.Factory(
        DicomService,
        patient_service=patient_service,
        study_service=study_service,
        serie_service=serie_service,
        instance_service=instance_service
    )


class Container(containers.DeclarativeContainer):
    """ declarative container """

    wiring_config = containers.WiringConfiguration(modules=[
        "tests.repositories.test_patient_repository",
        "tests.services.test_patient_service",

        "app.api.endpoints.patient_routers",
        "app.api.endpoints.study_routers",
        "app.api.endpoints.serie_routers",
        "app.api.endpoints.instance_routers",
        "app.api.endpoints.dicom_routers",
    ])

    gateways = providers.Container(Gateways)

    repositories = providers.Container(
        Repositories,
        gateways=gateways
    )

    services = providers.Container(
        Services,
        repositories=repositories
    )
