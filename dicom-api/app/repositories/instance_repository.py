from sqlalchemy.orm import Session
from app import models, schemas

class InstancesRepo:
    
        async def create(db: Session, item: schemas.InstancesCreate):
            db_item = models.Instances(seriesID=item.seriesID, filename=item.filename)
            db.add(db_item)
            db.commit()
            db.refresh(db_item)

            return db_item

        def fetch_all(db: Session, skip: int = 0, limit: int = 100):
            return db.query(models.Instances).offset(skip).limit(limit).all()

        def delete_by_series_id(db: Session, _id):
            db.query(models.Instances).filter(models.Instances.seriesID == _id).delete()