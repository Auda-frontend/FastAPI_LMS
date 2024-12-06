# student.py
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models
from app import schemas
from app.database import get_db
from app.models import BookIssue
from app.schemas import BookIssue, Student

router = APIRouter()

@router.get("/my-books", response_model=List[schemas.BookIssue])
def get_my_books(student_id: int, db: Session = Depends(get_db)):
    # Query the BookIssue table for books issued to the student
    books_issued = db.query(models.BookIssue).filter(models.BookIssue.student_id == student_id).all()

    # Return the list of BookIssue objects converted to Pydantic models
    return [schemas.BookIssue.from_orm(book_issue) for book_issue in books_issued]

