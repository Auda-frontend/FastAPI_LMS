# analytics.py
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Student, Book, BookIssue
from app.schemas import Analytics

router = APIRouter()

@router.get("/analytics", response_model=Analytics)
def get_analytics(db: Session = Depends(get_db)):
    total_students = db.query(Student).count()
    total_books = db.query(Book).count()
    total_issued_books = db.query(BookIssue).filter(BookIssue.return_date == None).count()
    total_overdue_books = db.query(BookIssue).filter(BookIssue.return_date < datetime.now()).count()
    
    return Analytics(
        total_students=total_students,
        total_books=total_books,
        total_issued_books=total_issued_books,
        total_overdue_books=total_overdue_books
    )
