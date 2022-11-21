from sqlalchemy.orm import Session
from app import models, schemas

class PatientsRepo:

    async def create(db: Session, item: schemas.PatientsCreate):
        db_item = models.Patients(patientID=item.patientID, name=item.name, birthDate=item.birthDate)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)

        return db_item

    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Patients).offset(skip).limit(limit).all()

    def fetch_by_id(db: Session, _id):
        return db.query(models.Patients).filter(models.Patients.patientID == _id).first()

    def fetch_patient_studies(db: Session, _id):
        return db.query(models.Studies).filter(models.Studies.patientID == _id).all()