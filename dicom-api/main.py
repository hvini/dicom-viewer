from app.repositories.instance_repository import InstancesRepo
from app.repositories.instance_repository import InstancesRepo
from fastapi import Depends, FastAPI, File, UploadFile, Form
from app.repositories.patient_repository import PatientsRepo
from app.repositories.study_repository import StudiesRepo
from app.repositories.serie_repository import SeriesRepo
from app.repositories.dicom_repository import DicomRepo
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from db import get_db, engine
import app.models as models
from app import schemas
from typing import List
import asyncio
import uvicorn
import os

app = FastAPI()

load_dotenv()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/bits", StaticFiles(directory="bits"), name="bits")

models.Base.metadata.create_all(bind=engine)

@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    return JSONResponse(status_code=500, content=jsonable_encoder({"code": "internal_error", "message": str(err)}))

### DICOMS ###
@app.post('/dicom/upload', tags=["Dicoms"])
async def upload_dicom(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    return await DicomRepo.upload(db=db, files=files)

@app.get('/dicom/3d', tags=["Dicoms"])
async def get_3d_data(path: str, bitspath: str, db: Session = Depends(get_db)):
    return await asyncio.run(DicomRepo.get_3d_data(dicoms_path=path, bits_path=bitspath, db=db))

### PATIENTS ###
@app.get('/patients', tags=["Patients"])
def get_patients(db: Session = Depends(get_db)):
    return PatientsRepo.fetch_all(db=db)

@app.get('/patients/{id}/studies', tags=["Patients"])
def get_patient_studies(id: int, db: Session = Depends(get_db)):
    return PatientsRepo.fetch_patient_studies(db=db, _id=id)

### STUDIES ###
@app.get('/studies', tags=["Studies"])
def get_studies(db: Session = Depends(get_db)):
    return StudiesRepo.fetch_all(db=db)

@app.get('/studies/{id}/series', tags=["Studies"])
def get_study_series(id: int, db: Session = Depends(get_db)):
    return StudiesRepo.fetch_study_series(db=db, _id=id)

### SERIES ###
@app.put('/series/{id}/update', response_model=schemas.Series)
async def update_series(id: int, item: schemas.SeriesUpdate, db: Session = Depends(get_db)):
    return await SeriesRepo.update(_id=id, db=db, item=item)

@app.get('/series', tags=["Series"])
def get_series(db: Session = Depends(get_db)):
    return SeriesRepo.fetch_all(db=db)

@app.get('/series/{id}/instances', tags=["Series"])
def get_series_instances(id: int, db: Session = Depends(get_db)):
    return SeriesRepo.fetch_serie_instances(db=db, _id=id)

### INSTANCES ###
@app.get('/instances', tags=["Instances"])
def get_instances(db: Session = Depends(get_db)):
    return InstancesRepo.fetch_all(db=db)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host='0.0.0.0',
        port=3000,
        #ssl_keyfile="./key.pem",
        #ssl_certfile="./cert.pem",
        reload=True
    )