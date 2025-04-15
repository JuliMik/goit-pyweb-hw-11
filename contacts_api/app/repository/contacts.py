from sqlalchemy.orm import Session
from app.models import Contact
from app.schemas import ContactCreate
from datetime import datetime, timedelta


# Функція для створення нового контакту
def create_contact(db: Session, contact: ContactCreate):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


# Отримати всі контакти з бази
def get_all_contacts(db: Session):
    return db.query(Contact).all()


# Отримати конкретний контакт за його ID
def get_contact_by_id(contact_id: int, db: Session):
    return db.query(Contact).filter(Contact.id == contact_id).first()


# Оновити контакт за ID
def update_contact(contact_id: int, contact: ContactCreate, db: Session):
    db_contact = get_contact_by_id(contact_id, db)
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
        return db_contact
    return None


# Видалення контакту за ID
def delete_contact(contact_id: int, db: Session):
    db_contact = get_contact_by_id(contact_id, db)
    if db_contact:
        db.delete(db_contact)
        db.commit()
        return db_contact
    return None


# Пошук контактів за ім'ям, прізвищем або email (усі параметри необов'язкові)
def search_contacts(first_name: str = None, last_name: str = None, email: str = None, db: Session = None):
    query = db.query(Contact)

    if first_name:
        query = query.filter(Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))

    return query.all()


# Отримати список контактів, у яких день народження припадає на найближчі 7 днів
def get_upcoming_birthdays(db: Session):
    today = datetime.today().date()
    end_date = today + timedelta(days=7)

    contacts = db.query(Contact).all()
    upcoming = []

    for contact in contacts:
        bday = contact.birth_date.replace(year=today.year)
        if today <= bday <= end_date:
            upcoming.append(contact)

    return upcoming
