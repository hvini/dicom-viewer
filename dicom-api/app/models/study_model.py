""" study model """

from sqlalchemy import Column, ForeignKey, Integer, String
from db import Base


class Study(Base):
    """ study model class """

    __tablename__ = "studies"

    id = Column(Integer, primary_key=True, index=True)
    patientID = Column(Integer, ForeignKey("patients.id"), nullable=False)
    instanceUID = Column(String, nullable=False)
    description = Column(String, nullable=False)
    time = Column(String, nullable=False)

    def __repr__(self):
        return f"<Studies(instanceUID={self.instanceUID},\
                           description={self.description},\
                           time={self.time})>"
