from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, database
from app.schemas import ContactResponse, ContactCreate
from app.repository import contacts

router = APIRouter(prefix="/contacts", tags=["Contacts"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Пошук контактів
@router.get("/search", response_model=list[ContactResponse])
def search_contacts(
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        db: Session = Depends(get_db)
):
    db_contacts = contacts.search_contacts(first_name, last_name, email, db)
    return db_contacts


# Створення контакту
@router.post("/", response_model=schemas.ContactResponse)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    db_contact = models.Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


# Отримання контакту за ID
@router.get("/{contact_id}", response_model=ContactResponse)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = contacts.get_contact_by_id(contact_id, db)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


# Отримання списку всіх контактів
@router.get("/", response_model=list[ContactResponse])
def get_contacts(db: Session = Depends(get_db)):
    db_contacts = contacts.get_all_contacts(db)
    return db_contacts


# Оновлення контакту
@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = contacts.get_contact_by_id(contact_id, db)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    for key, value in contact.dict().items():
        setattr(db_contact, key, value)

    db.commit()
    db.refresh(db_contact)
    return db_contact


# Видалення контакту
@router.delete("/{contact_id}", response_model=ContactResponse)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = contacts.get_contact_by_id(contact_id, db)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    db.delete(db_contact)
    db.commit()
    return db_contact


# Отримання контактів з днями народження на найближчі 7 днів
@router.get("/birthdays/", response_model=List[ContactResponse])
def upcoming_birthdays(db: Session = Depends(get_db)):
    return contacts.get_upcoming_birthdays(db)
