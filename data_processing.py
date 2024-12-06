import requests
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# API Endpoints
books_api = "http://localhost:8000/admin/available_books/"
students_api = "http://localhost:8000/admin/students/"
issues_api = "http://localhost:8000/admin/issued_books/"

# Function to fetch data
def fetchdata(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

# Fetching data
books_data = fetchdata(books_api)
students_data = fetchdata(students_api)
issues_data = fetchdata(issues_api)

# Creating DataFrames
books_df = pd.DataFrame(books_data)
students_df = pd.DataFrame(students_data)
issues_df = pd.DataFrame(issues_data)

# Handling missing values in 'issues_df'
issues_df["return_date"] = issues_df["return_date"].fillna("Not Returned")

# Drop rows with missing data in 'books_df' and 'students_df'
students_df.dropna(inplace=True)
books_df.dropna(inplace=True)

# Standardize student names and emails
students_df['name'] = students_df['name'].str.strip().str.title()
students_df['email'] = students_df['email'].str.strip().str.lower()

# Add membership start dates and calculate membership duration
students_df['membership_start'] = pd.to_datetime(['2023-01-01', '2022-05-10', '2023-03-15'], errors='coerce')
students_df['membership_duration_days'] = (pd.Timestamp.now() - students_df['membership_start']).dt.days

# Feature engineering for books: calculate 'total_copies' and 'availability_ratio'
issued_counts = issues_df.groupby('book_id').size().rename('issued_copies')
books_df = books_df.merge(issued_counts, how='left', left_on='id', right_on='book_id')
books_df['issued_copies'] = books_df['issued_copies'].fillna(0).astype(int)
books_df['total_copies'] = books_df['available_copies'] + books_df['issued_copies']
books_df['availability_ratio'] = books_df['available_copies'] / books_df['total_copies']

# Extract issue date details
issues_df['issue_date'] = pd.to_datetime(issues_df['issue_date'], errors='coerce')
issues_df['return_date'] = pd.to_datetime(issues_df['return_date'], errors='coerce', format='%Y-%m-%d')
issues_df['issue_year'] = issues_df['issue_date'].dt.year
issues_df['issue_month'] = issues_df['issue_date'].dt.month
issues_df['issue_day'] = issues_df['issue_date'].dt.day

# Merge DataFrames
merged_df = pd.merge(issues_df, books_df, left_on="book_id", right_on="id", how="inner")
merged_df = pd.merge(merged_df, students_df, left_on="student_id", right_on="id", how="inner", suffixes=('_book', '_student'))

# Normalize numerical data
numeric_columns = merged_df.select_dtypes(include=['int64', 'float64']).columns
scaler = MinMaxScaler()
merged_df[numeric_columns] = scaler.fit_transform(merged_df[numeric_columns])

# Display DataFrames
print("Books DataFrame after Feature Engineering:")
print(books_df.head())
print(books_df.info())

print("Students DataFrame after Feature Engineering:")
print(students_df.head())
print(students_df.info())

print("Issues DataFrame after Feature Engineering:")
print(issues_df.head())
print(issues_df.info())

print("Merged DataFrame after Normalization:")
print(merged_df.head())
print(merged_df.info())
