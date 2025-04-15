from . import models
from .database import engine
from .routes import contacts
from fastapi import FastAPI

# Створення всіх таблиць у базі даних на основі моделей
models.Base.metadata.create_all(bind=engine)

# Ініціалізація FastAPI-додатку
app = FastAPI()


# Головний маршрут (корінь) — повертає привітальне повідомлення
@app.get("/")
def read_root():
    return {"message": "Welcome to the contacts API, my homework!"}


# Підключення маршруту для контактів (CRUD та додаткові функції)
app.include_router(contacts.router)
