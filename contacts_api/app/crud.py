from sqlalchemy.orm import Session
from . import models, schemas


# Створення нового контакту в базі даних
def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = models.Contact(
        first_name=contact.first_name,
        last_name=contact.last_name,
        email=contact.email,
        phone_number=contact.phone_number,
        birth_date=contact.birth_date,
        additional_info=contact.additional_info
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


# Отримання списку контактів з можливістю пагінації (skip, limit)
def get_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Contact).offset(skip).limit(limit).all()
