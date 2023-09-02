""" patient model """

from sqlalchemy import Column, Integer, String
from db import Base


class Patient(Base):
    """ patient model class """
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    patientID = Column(String, nullable=False)
    name = Column(String, nullable=False)
    birthDate = Column(String, nullable=False)

    def __repr__(self):
        return f"<Patients(name={self.name}, birthDate={self.birthDate})>"
