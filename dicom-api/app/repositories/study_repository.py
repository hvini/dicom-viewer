from sqlalchemy.orm import Session
from app import models, schemas

class StudiesRepo:

    async def create(db: Session, item: schemas.StudiesCreate):
        db_item = models.Studies(instanceUID=item.instanceUID, patientID=item.patientID, description=item.description, time=item.time)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)

        return db_item

    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Studies).offset(skip).limit(limit).all()

    def fetch_by_id(db: Session, _id):
        return db.query(models.Studies).filter(models.Studies.instanceUID == _id).first()

    def fetch_study_series(db: Session, _id):
        return db.query(models.Series).filter(models.Series.studyID == _id).all()