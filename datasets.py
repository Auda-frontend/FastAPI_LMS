import pandas as pd
import random
import requests
from datetime import datetime

# Step 1: Generate dataset for books
def generate_books_dataset(rows=20):
    data = {
        "id": [num for num in range(1, rows + 1)],  
        "title": [f"Book Title {num}" for num in range(1, rows + 1)],  
        "author": [f"Author {random.choice(range(1, 10))}" for _ in range(rows)],  
        "available_copies": [random.randint(1, 10) for _ in range(rows)],  
    }
    return pd.DataFrame(data)

# Step 1.1: Post data to FastAPI
def post_data_to_api(df):

    api_url = "http://127.0.0.1:8000/admin/add_book"  
    for _, row in df.iterrows():

        book_data = row.to_dict()

        try:
            response = requests.post(api_url, json=book_data)
            response.raise_for_status()  
            print(f"Successfully uploaded book: {book_data['title']}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to upload book: {book_data['title']}\nError: {e}")
            continue  

# Step 2: Describe the dataset
def describe_books_dataset(df):
    return df.describe(include="all")

# Step 3: Handle null values
def handle_null_values(df):

    df.loc[random.sample(range(len(df)), 5), "available_copies"] = None  
    print("\nMissing Values Before Handling:")
    print(df.isnull().sum())

    df["available_copies"] = df["available_copies"].fillna(0)  
    print("\nMissing Values After Handling:")
    print(df.isnull().sum())
    return df

# Step 4: Perform basic data processing
def process_books_data(df):

    available_books = df[df["available_copies"] > 0]
    return df, available_books

# Step 5: Create new features
def create_new_features(df):
    # Feature 1: "is_popular" based on available copies (more than 5 copies considered popular)
    df["is_popular"] = df["available_copies"] > 5
    # Feature 2: "is_new" based on publishing year (books published in the last 3 years are considered new)
    df["is_new"] = df["available_copies"] > 0  
    return df


# Main execution
if __name__ == "__main__":

    print("Generating books dataset...")
    df_books = generate_books_dataset()
    print("Dataset Shape:", df_books.shape)
    

    print("\nBooks Dataset Description:")
    print(describe_books_dataset(df_books))
    

    print("\nHandling Null Values...")
    df_books = handle_null_values(df_books)
    

    print("\nProcessing Data...")
    df_books, available_books = process_books_data(df_books)
    print(f"\nAvailable Books: {len(available_books)}")
    

    print("\nCreating New Features...")
    df_books = create_new_features(df_books)


    print("\nSaving Processed Dataset to 'books_dataset.csv'...")
    df_books.to_csv("books_dataset.csv", index=False)
    print("Dataset saved successfully.")

    print("\nData processing completed!")
