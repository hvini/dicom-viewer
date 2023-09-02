""" study schema """

from pydantic import BaseModel


class StudyBase(BaseModel):
    """ study base """

    instanceUID: str
    patientID: int
    description: str
    time: str


class StudyCreate(StudyBase):
    """ study create """


class Study(StudyBase):
    """ study """

    id: int

    class Config:
        """ config """

        orm_mode = True
