import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

class LibraryManagementAnalyzer:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.books_df = None
        self.students_df = None
        self.issues_df = None

    def fetch_data(self):
        """Fetch and prepare data from all endpoints"""
        try:
        # Fetch and validate books data
            books_response = requests.get(f"{self.base_url}/admin/available_books/")
            books_data = books_response.json()
            if books_data:
                self.books_df = pd.DataFrame(books_data)

        # Fetch and validate students data
            students_response = requests.get(f"{self.base_url}/admin/students/")
            students_data = students_response.json()
            if students_data:
                self.students_df = pd.DataFrame(students_data)

        # Fetch and validate book issues data
            issues_response = requests.get(f"{self.base_url}/admin/issued_books/")
            issues_data = issues_response.json()
            if issues_data:
                self.issues_df = pd.DataFrame(issues_data)

        # Process issues data
            if self.issues_df is not None and not self.issues_df.empty:
                self.issues_df['issue_date'] = pd.to_datetime(self.issues_df['issue_date'])
                self.issues_df['return_date'] = pd.to_datetime(self.issues_df['return_date'])

        except Exception as e:
            print(f"Error fetching data: {str(e)}")


    def analyze_books(self):
        """Analyze book-related data"""
        if self.books_df is None or self.books_df.empty:
            print("No books data available")
            return

        print("\n=== Book Analysis ===")
        print(f"Total Books: {len(self.books_df)}")
        print(f"Total Available Copies: {self.books_df['available_copies'].sum()}")

        most_popular_books = self.issues_df['book_id'].value_counts().head(5)
        print("\nMost Issued Books:")
        for book_id, count in most_popular_books.items():
            book_title = self.books_df.loc[self.books_df['id'] == book_id, 'title'].values[0]
            print(f"{book_title}: {count} issues")

    def analyze_students(self):
        """Analyze student-related data"""
        if self.students_df is None or self.students_df.empty:
            print("No students data available")
            return

        print("\n=== Student Analysis ===")
        print(f"Total Students: {len(self.students_df)}")

        active_students = self.issues_df['student_id'].value_counts().head(5)
        print("\nMost Active Students:")
        for student_id, count in active_students.items():
            student_name = self.students_df.loc[self.students_df['id'] == student_id, 'name'].values[0]
            print(f"{student_name}: {count} books issued")

    def analyze_book_issues(self):
        """Analyze book issue and return patterns"""
        if self.issues_df is None or self.issues_df.empty:
            print("No book issue data available")
            return

        print("\n=== Book Issue Analysis ===")
        print(f"Total Book Issues: {len(self.issues_df)}")

        # Overdue books
        today = datetime.now()
        self.overdue_issues = self.issues_df[(self.issues_df['return_date'].isna()) &
                                        (self.issues_df['issue_date'] + timedelta(days=14) < today)]
        print(f"Overdue Books: {len(self.overdue_issues)}")

        # Issues by day
        self.issues_df['day_name'] = self.issues_df['issue_date'].dt.day_name()
        print("\nIssues by Day:")
        day_counts = self.issues_df['day_name'].value_counts()
        for day, count in day_counts.items():
            print(f"{day}: {count} issues")

    def make_insights(self):
        """Generate business insights from the data"""
        print("\n=== Library Insights ===")

        if not self.issues_df.empty:
            # Peak issue days
            busy_days = self.issues_df['issue_date'].dt.day_name().value_counts().idxmax()
            print(f"Most Active Day: {busy_days}")

            # Student activity
            avg_books_per_student = len(self.issues_df) / len(self.students_df)
            print(f"Average Books Issued Per Student: {avg_books_per_student:.2f}")

            # Overdue rate
            overdue_rate = (len(self.overdue_issues) / len(self.issues_df)) * 100
            print(f"Overdue Rate: {overdue_rate:.1f}%")


def main():
    analyzer = LibraryManagementAnalyzer()
    print("Fetching and analyzing data...")
    analyzer.fetch_data()

    # Run analyses
    analyzer.analyze_books()
    analyzer.analyze_students()
    analyzer.analyze_book_issues()
    analyzer.make_insights()

if __name__ == "__main__":
    main()
