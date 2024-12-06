from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Base Book Schema
class BookBase(BaseModel):
    title: str
    author: str
    available_copies: int

    class Config:
        orm_mode = True
        from_attributes = True

# Book Creation Schema
class BookCreate(BookBase):
    pass

# Book Response Schema
class Book(BookBase):
    id: int

# Base Student Schema
class StudentBase(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True

# Student Response Schema
class Student(StudentBase):
    id: int

# Schema for Students with Books (Optional Usage)
class StudentWithBooks(Student):
    books: List[Book] = []

    class Config:
        orm_mode = True
        from_attributes = True

# Base Book Issue Schema
class BookIssueBase(BaseModel):
    book_id: int
    student_id: int
    issued_by: int
    issue_date: datetime
    return_date: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True

# Book Issue Creation Schema
class BookIssueCreate(BookIssueBase):
    pass

# Book Issue Response Schema
class BookIssue(BookIssueBase):
    id: int

# Analytics Schema
class Analytics(BaseModel):
    total_students: int
    total_books: int
    total_issued_books: int
    total_overdue_books: int

    class Config:
        orm_mode = True
