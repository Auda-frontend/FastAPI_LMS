from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, database, schemas  # Make sure to import your models and schemas
from typing import List
from sqlalchemy.orm import joinedload

router = APIRouter()

# Dependency for getting the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. View Available Books
@router.get("/available_books", response_model=List[schemas.Book])
def get_available_books(db: Session = Depends(get_db)):
    available_books = db.query(models.Book).filter(models.Book.available_copies > 0).all()
    return available_books

# 2. View Students
@router.get("/students", response_model=List[schemas.Student])
def get_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    return students

# 3. View Issued Books with Students
@router.get("/issued_books", response_model=List[schemas.BookIssueBase])
def get_issued_books(db: Session = Depends(get_db)):
    issued_books = db.query(models.BookIssue).join(models.Student).join(models.Book).all()
    return issued_books

# 4. Add New Book (Admin functionality)
@router.post("/add_book", response_model=schemas.Book)
def add_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = models.Book(**book.dict())
    
    # Check if the book already exists
    existing_book = db.query(models.Book).filter(models.Book.title == book.title).first()
    if existing_book:
        raise HTTPException(status_code=400, detail="Book already exists")

    db.add(db_book)
    db.commit()
    
    return db_book

# 5. Issue Book to Student (Admin functionality)
@router.post("/issue_book", response_model=schemas.BookIssue)
def issue_book(issue: schemas.BookIssueCreate, db: Session = Depends(get_db)):
    # Check if the book is available
    book = db.query(models.Book).filter(models.Book.id == issue.book_id).first()
    if not book or book.available_copies == 0:
        raise HTTPException(status_code=400, detail="Book is not available for issuing")

    # Check if the student exists
    student = db.query(models.Student).filter(models.Student.id == issue.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Create a new BookIssue entry
    db_issue = models.BookIssue(
        book_id=issue.book_id,
        student_id=issue.student_id,
        issued_by=issue.issued_by,
        issue_date=issue.issue_date,
        return_date=issue.return_date
    )
    
    # Update the book's available copies
    book.available_copies -= 1

    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)

    return db_issue
