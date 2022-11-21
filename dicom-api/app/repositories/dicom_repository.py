from app.repositories.instance_repository import InstancesRepo
from app.repositories.patient_repository import PatientsRepo
from app.repositories.study_repository import StudiesRepo
from app.repositories.serie_repository import SeriesRepo
from utils.dicom import getAllData, to3dArray
from fastapi.responses import JSONResponse
from fastapi import File, UploadFile
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import models, schemas
from pathlib import Path
from typing import List
import numpy as np
import json
import sys
import os

class DicomRepo:

    async def upload(db: Session, files: List[UploadFile] = File(...)):
        
        slices = getAllData(files=files)

        patientID = slices[0].PatientID
        patient = PatientsRepo.fetch_by_id(db, patientID)
        if (patient is None):
            patientName = str(slices[0].PatientName)
            patientBirthDate = slices[0].PatientBirthDate

            patient = await PatientsRepo.create(db=db, item=schemas.PatientsCreate(patientID=patientID, name=patientName, birthDate=patientBirthDate))

        studyInstanceUID = slices[0].StudyInstanceUID
        study = StudiesRepo.fetch_by_id(db, studyInstanceUID)
        if (study is None):
            studyDescription = slices[0].StudyDescription
            studyTime = slices[0].StudyTime

            study = await StudiesRepo.create(db=db, item=schemas.StudiesCreate(instanceUID=studyInstanceUID, patientID=patient.id, description=studyDescription, time=studyTime))

        seriesInstanceUID = slices[0].SeriesInstanceUID
        series = SeriesRepo.fetch_by_id(db, seriesInstanceUID)

        destination = Path(f'./dicoms/{patient.patientID}/{study.instanceUID}/{seriesInstanceUID}')
        if (series is None):
            seriesDescription = slices[0].SeriesDescription

            series = await SeriesRepo.create(db=db, item=schemas.SeriesCreate(instanceUID=seriesInstanceUID, studyID=study.id, filepath=str(destination), description=seriesDescription))
        
        isExists = os.path.exists(destination)
        if not isExists:
            os.makedirs(destination)

        InstancesRepo.delete_by_series_id(db=db, _id=series.id)
        for i, slice in enumerate(slices):
            filename = files[i].filename
            await InstancesRepo.create(db=db, item=schemas.InstancesCreate(seriesID=series.id, filename=filename))
            
            path = f'{destination}/{filename}'
            slice.save_as(path)

        return JSONResponse(status_code=201, content={'success': True, 'message': 'Files uploaded successfully'})

    async def get_3d_data(dicoms_path: str, bits_path: str, db: Session):
        slices = getAllData(path=dicoms_path)

        dimX = slices[0].Rows
        dimY = slices[0].Columns
        dimZ = len(slices)

        pixelSpacing = slices[0].PixelSpacing[0]

        scaleX = 0
        scaleY = 0
        scaleZ = 0
        if (pixelSpacing > 0):
            scaleX = pixelSpacing * dimX
            scaleY = pixelSpacing * dimY
            scaleZ = abs(slices[len(slices) - 1].SliceLocation - slices[0].SliceLocation)

        if (bits_path):
            resp = {
                'dimX': dimX,
                'dimY': dimY,
                'dimZ': dimZ,
                'pixelSpacing': pixelSpacing,
                'scaleX': scaleX,
                'scaleY': scaleY,
                'scaleZ': scaleZ
            }

            serialized_data = json.dumps(resp)
            return JSONResponse(status_code=200, content=json.loads(serialized_data))
        else:
            img3d = to3dArray(slices)
            data = img3d.ravel().tolist()

            minDataValue =  float("3.40282347e38")
            maxDataValue = float("-3.40282347e38")

            minVal = min(data)
            maxVal = max(data)

            minDataValue = min([minDataValue, minVal])
            maxDataValue = max([maxDataValue, maxVal])
            maxRange = maxDataValue - minDataValue

            sampleSize = 2
            bytesArr = np.zeros(len(data) * sampleSize)
            for i, d in enumerate(data):
                pixelValue = (d - minDataValue) / maxRange
                bytesArr[i] = pixelValue

            seriesInstanceUID = dicoms_path.split('/')[3]
            bitspath = 'bits/' + seriesInstanceUID + '.bits'
            with open(bitspath, 'wb') as fsave:
                fsave.write(np.float16(bytesArr).tobytes())
            
            series = db.query(models.Series).filter(models.Series.instanceUID == seriesInstanceUID).first()
            if not series:
                raise HTTPException(status_code=404, detail="Series not found")
                
            series.bitspath = bitspath
            
            db.commit()

            resp = {
                'dimX': dimX,
                'dimY': dimY,
                'dimZ': dimZ,
                'pixelSpacing': pixelSpacing,
                'scaleX': scaleX,
                'scaleY': scaleY,
                'scaleZ': scaleZ,
                'bitspath': bitspath
            }

            serialized_data = json.dumps(resp)
            return JSONResponse(status_code=200, content=json.loads(serialized_data))