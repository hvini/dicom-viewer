from typing import List, Optional
from pydantic import BaseModel

class SeriesBase(BaseModel):
    instanceUID: str
    studyID: int
    filepath: str
    description: str

class SeriesCreate(SeriesBase):
    pass

class SeriesUpdate(SeriesBase):
    id: int
    bitspath: str

class Series(SeriesBase):
    id: int

    class Config:
        orm_mode = True

class InstancesBase(BaseModel):
    seriesID: int
    filename: str

class InstancesCreate(InstancesBase):
    pass

class Instances(InstancesBase):
    id: int

    class Config:
        orm_mode = True

class StudiesBase(BaseModel):
    instanceUID: str
    patientID: int
    description: str
    time: str

class StudiesCreate(StudiesBase):
    pass

class Studies(StudiesBase):
    id: int

    class Config:
        orm_mode = True


class PatientsBase(BaseModel):
    patientID: str
    name: str
    birthDate: str

class PatientsCreate(PatientsBase):
    pass

class Patients(PatientsBase):
    id: int

    class Config:
        orm_mode = True