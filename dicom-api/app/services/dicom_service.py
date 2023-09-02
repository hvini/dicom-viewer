""" dicom service module """

from pathlib import Path
from typing import List
import os
from fastapi import File, UploadFile
import numpy as np
from app.services.instance_service import InstanceService
from app.services.patient_service import PatientService
from app.services.study_service import StudyService
from app.services.serie_service import SerieService
from app.utils.dicom import get_all_data, to_3d_array
from app.schemas.patient_schema import PatientCreate
from app.schemas.study_schema import StudyCreate
from app.schemas.serie_schema import SerieCreate, SerieUpdate
from app.schemas.instance_schema import InstanceCreate
from app.errors import NotFoundException
from google.cloud import storage

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "dicom-api-83e532ca4b71.json"
client = storage.Client()
bucket = client.bucket("dicom-api")

class DicomService:
    """ dicom service class """

    def __init__(self, patient_service: PatientService,
                 study_service: StudyService,
                 serie_service: SerieService,
                 instance_service: InstanceService) -> None:
        self._patient_service: PatientService = patient_service
        self._study_service: StudyService = study_service
        self._serie_service: SerieService = serie_service
        self._instance_service: InstanceService = instance_service

    async def upload(self, files: List[UploadFile] = File(...)) -> None:
        """ upload dicom dir """

        slices = get_all_data(files=files)

        patient_id = slices[0].PatientID
        try:
            patient = self._patient_service.fetch_by_id(patient_id)
        except NotFoundException:
            patient_name = str(slices[0].PatientName)
            patient_birth_date = slices[0].PatientBirthDate

            patient = await self._patient_service.create(
                PatientCreate(patientID=patient_id,
                              name=patient_name,
                              birthDate=patient_birth_date))

        study_instance_uid = slices[0].StudyInstanceUID
        try:
            study = self._study_service.fetch_by_id(study_instance_uid)
        except NotFoundException:
            study_description = slices[0].StudyDescription
            study_time = slices[0].StudyTime

            study = await self._study_service.create(
                StudyCreate(instanceUID=study_instance_uid,
                            patientID=patient.id,
                            description=study_description,
                            time=study_time))

        serie_instance_uid = slices[0].SeriesInstanceUID
        destination = Path(
            f"./dicoms/{patient.patientID}/{study.instanceUID}/{serie_instance_uid}")
        try:
            series = self._serie_service.fetch_by_id(serie_instance_uid)
        except NotFoundException:
            serie_description = slices[0].SeriesDescription

            dim_x = slices[0].Rows
            dim_y = slices[0].Columns
            dim_z = len(slices)

            pixel_spacing = slices[0].PixelSpacing[0]

            scale_x = 0
            scale_y = 0
            scale_z = 0
            if pixel_spacing > 0:
                scale_x = pixel_spacing * dim_x
                scale_y = pixel_spacing * dim_y
                scale_z = abs(
                    slices[len(slices) - 1].SliceLocation - slices[0].SliceLocation)

            series = await self._serie_service.create(
                SerieCreate(instanceUID=serie_instance_uid,
                            studyID=study.id,
                            filepath=str(destination),
                            description=serie_description,
                            dimX=dim_x,
                            dimY=dim_y,
                            dimZ=dim_z,
                            pixelSpacing=pixel_spacing,
                            scaleX=scale_x,
                            scaleY=scale_y,
                            scaleZ=scale_z),
            )

        is_exists = os.path.exists(destination)
        if not is_exists:
            os.makedirs(destination)

        try:
            self._instance_service.delete_by_serie_id(series.id)
        except NotFoundException:
            pass

        for i, slice in enumerate(slices):
            filename = files[i].filename
            await self._instance_service.create(
                InstanceCreate(seriesID=series.id, filename=filename))

            path = f'{destination}/{filename}'
            slice.save_as(path)

    async def generate_bits(self, serie_id) -> any:
        """ generate bits file """

        serie = self._serie_service.fetch_by_id(serie_id)
        slices = get_all_data(path=serie.filepath)
        img3d = to_3d_array(slices)
        data = img3d.ravel().tolist()

        min_data_value = float("3.40282347e38")
        max_data_value = float("-3.40282347e38")

        min_val = min(data)
        max_val = max(data)

        min_data_value = min([min_data_value, min_val])
        max_data_value = max([max_data_value, max_val])
        max_range = max_data_value - min_data_value

        sample_size = 2
        bytes_arr = np.zeros(len(data) * sample_size)
        for i, d in enumerate(data):
            pixel_value = (d - min_data_value) / max_range
            bytes_arr[i] = pixel_value

        is_exists = os.path.exists('./bits')
        if not is_exists:
            os.makedirs('./bits')

        bitspath = 'bits/' + serie.instanceUID + '.bits'
        with open(bitspath, 'wb') as fsave:
            fsave.write(np.float16(bytes_arr).tobytes())

        blob = bucket.blob(bitspath)
        blob.upload_from_filename(bitspath)
        bits_url = blob.public_url

        os.remove(bitspath)

        updated = await self._serie_service.update(
            SerieUpdate(
                instanceUID=serie.instanceUID,
                studyID=serie.studyID,
                filepath=serie.filepath,
                description=serie.description,
                bitspath=bits_url,
                dimX=serie.dimX,
                dimY=serie.dimY,
                dimZ=serie.dimZ,
                pixelSpacing=serie.pixelSpacing,
                scaleX=serie.scaleX,
                scaleY=serie.scaleY,
                scaleZ=serie.scaleZ,
            ), serie.instanceUID)

        return updated
