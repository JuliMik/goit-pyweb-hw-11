from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


# Схема для створення нового контакту
class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birth_date: date
    additional_info: Optional[str] = None


# Схема відповіді при отриманні контакту
class ContactResponse(ContactCreate):
    id: int

    class Config:
        from_attributes = True
