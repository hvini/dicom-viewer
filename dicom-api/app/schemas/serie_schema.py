""" serie schema """

from pydantic import BaseModel


class SerieBase(BaseModel):
    """ serie base """

    instanceUID: str
    studyID: int
    filepath: str
    description: str
    dimX: str
    dimY: str
    dimZ: str
    pixelSpacing: str
    scaleX: str
    scaleY: str
    scaleZ: str


class SerieCreate(SerieBase):
    """ serie create """


class SerieUpdate(SerieBase):
    """ serie update """

    bitspath: str


class Serie(SerieBase):
    """ serie """

    id: int

    class Config:
        """ config """

        orm_mode = True
