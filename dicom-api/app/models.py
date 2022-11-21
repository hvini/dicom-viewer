from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from db import Base

class Series(Base):
    __tablename__ = "series"

    id = Column(Integer, primary_key=True, index=True)
    studyID = Column(Integer, ForeignKey("studies.id"))
    instanceUID = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    bitspath = Column(String, nullable=True)
    description = Column(String, nullable=False)
    
    def __repr__(self):
        return "<Series(instanceUID='%s', description='%s')>" % (self.instanceUID, self.description)

class Instances(Base):
    __tablename__ = "instances"

    id = Column(Integer, primary_key=True, index=True)
    seriesID = Column(Integer, ForeignKey("series.id"), nullable=False)
    filename = Column(String, nullable=False)
    
    def __repr__(self):
        return "<Instances(seriesID='%s', filename='%s')>" % (self.seriesID, self.filename)

class Studies(Base):
    __tablename__ = "studies"

    id = Column(Integer, primary_key=True, index=True)
    patientID = Column(Integer, ForeignKey("patients.id"), nullable=False)
    instanceUID = Column(String, nullable=False)
    description = Column(String, nullable=False)
    time = Column(String, nullable=False)

    def __repr__(self):
        return "<Studies(instanceUID='%s', description='%s', time='%s')>" % (self.instanceUID, self.description, self.time)

class Patients(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    patientID = Column(String, nullable=False)
    name = Column(String, nullable=False)
    birthDate = Column(String, nullable=False)

    def __repr__(self):
        return "<Patients(name='%s', birthDate='%s')>" % (self.name, self.birthDate)