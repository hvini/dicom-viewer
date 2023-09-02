""" serie model """

from sqlalchemy import Column, ForeignKey, Integer, String
from db import Base


class Serie(Base):
    """ study model class """

    __tablename__ = "series"

    id = Column(Integer, primary_key=True, index=True)
    studyID = Column(Integer, ForeignKey("studies.id"))
    instanceUID = Column(String, nullable=False)
    description = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    bitspath = Column(String, nullable=True)
    dimX = Column(String, nullable=False)
    dimY = Column(String, nullable=False)
    dimZ = Column(String, nullable=False)
    pixelSpacing = Column(String, nullable=False)
    scaleX = Column(String, nullable=False)
    scaleY = Column(String, nullable=False)
    scaleZ = Column(String, nullable=False)

    def __repr__(self):
        return f"<Serie(id={self.id}, instanceUID={self.instanceUID}, studyID={self.studyID}, description={self.description}, filepath={self.filepath}, bitspath={self.bitspath}, dimX={self.dimX}, dimY={self.dimY}, dimZ={self.dimZ}, pixelSpacing={self.pixelSpacing}, scaleX={self.scaleX}, scaleY={self.scaleY}, scaleZ={self.scaleZ})>"
