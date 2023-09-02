""" instance schema """

from pydantic import BaseModel


class InstanceBase(BaseModel):
    """ instance base """

    seriesID: int
    filename: str


class InstanceCreate(InstanceBase):
    """ instance create """


class Instance(InstanceBase):
    """ instance """

    id: int

    class Config:
        """ config """

        orm_mode = True
