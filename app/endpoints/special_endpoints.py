# special_endpoints.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models
from app import schemas
from app.database import get_db
from app.models import Student, Book, BookIssue
from app.schemas import StudentWithBooks

router = APIRouter()

@router.get("/students/{student_id}/books", response_model=schemas.StudentWithBooks)
def get_student_books(student_id: int, db: Session = Depends(get_db)):
    # Fetch the student
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Fetch books issued to the student
    books_issued = db.query(models.Book).join(models.BookIssue).filter(models.BookIssue.student_id == student_id).all()

    # Return the student with the list of books issued to them
    return schemas.StudentWithBooks(
        id=student.id,
        name=student.name,
        email=student.email,
        books=[schemas.Book.from_orm(book) for book in books_issued]  # Using from_orm to convert SQLAlchemy objects to Pydantic models
    )

@router.get("/issued_books", response_model=List[schemas.BookIssueBase])
def get_issued_books(db: Session = Depends(get_db)):
    issued_books = db.query(models.BookIssue).join(models.Student).join(models.Book).all()
    return issued_books