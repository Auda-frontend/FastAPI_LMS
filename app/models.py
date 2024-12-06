from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    # Many-to-many relationship with books via BookIssue
    books = relationship("Book", secondary="book_issues", back_populates="students")
    issued_books = relationship("BookIssue", back_populates="student")  # Direct relationship with BookIssue

class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    available_copies = Column(Integer, default=0)

    # Many-to-many relationship with students via BookIssue
    students = relationship("Student", secondary="book_issues", back_populates="books")
    issued_books = relationship("BookIssue", back_populates="book")  # Direct relationship with BookIssue

class BookIssue(Base):
    __tablename__ = 'book_issues'
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    issued_by = Column(Integer, ForeignKey('admins.id'), nullable=False)
    issue_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime)

    # Relationships
    book = relationship("Book", back_populates="issued_books")  # Links to Book
    student = relationship("Student", back_populates="issued_books")  # Links to Student
