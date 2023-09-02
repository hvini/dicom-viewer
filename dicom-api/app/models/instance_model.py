""" instance model """

from sqlalchemy import Column, ForeignKey, Integer, String
from db import Base


class Instance(Base):
    """ instance model class """
    __tablename__ = "instances"

    id = Column(Integer, primary_key=True, index=True)
    seriesID = Column(Integer, ForeignKey("series.id"), nullable=False)
    filename = Column(String, nullable=False)

    def __repr__(self):
        return f"<Instances(seriesID={self.seriesID}, filename={self.filename})>"
