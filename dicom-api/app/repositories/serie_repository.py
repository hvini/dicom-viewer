from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException

class SeriesRepo:

    async def create(db: Session, item: schemas.SeriesCreate):
        db_item = models.Series(instanceUID=item.instanceUID, studyID=item.studyID, filepath=item.filepath, description=item.description)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        
        return db_item

    async def update(_id, db: Session, item: schemas.SeriesUpdate):
        series = db.query(models.Series).filter(models.Series.id == _id).first()
        if not series:
            raise HTTPException(status_code=404, detail="Series not found")
            
        series.bitspath = item.bitspath
        
        db.commit()
        db.refresh(series)

        return series

    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Series).offset(skip).limit(limit).all()

    def fetch_by_id(db: Session, _id):
        return db.query(models.Series).filter(models.Series.instanceUID == _id).first()

    def fetch_serie_instances(db: Session, _id):
        return db.query(models.Instances).filter(models.Instances.seriesID == _id).all()