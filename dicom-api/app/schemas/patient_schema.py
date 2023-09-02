""" patient schema """

from pydantic import BaseModel


class PatientBase(BaseModel):
    """ patient base """

    patientID: str
    name: str
    birthDate: str


class PatientCreate(PatientBase):
    """ patient create """


class Patient(PatientBase):
    """ patient """

    id: int

    class Config:
        """ config """

        orm_mode = True
