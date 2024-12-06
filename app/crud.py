from sqlalchemy.orm import Session
from app import models, schemas

def get_students_with_books(db: Session):
    return db.query(models.Student).join(models.BookIssue).all()

def get_books_with_students(db: Session):
    return db.query(models.Book).join(models.BookIssue).all()
