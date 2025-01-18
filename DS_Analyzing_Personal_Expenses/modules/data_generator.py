import sqlite3
from faker import Faker
from datetime import date
import random
import os
import calendar

faker = Faker()


def create_table_for_month(conn, month_name):
    """Create a table for a specific month."""
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {month_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            payment_mode TEXT NOT NULL,
            cashback REAL DEFAULT 0
        );
    """)
    conn.commit()


def generate_monthly_expenses(month, year, num_records=100):
    """Generate random expense data for a specific month."""
    data = []
    for _ in range(num_records):
        data.append((
            faker.date_between_dates(
                date_start=date(year, month, 1),
                date_end=date(year, month, 28)  # Assumes 28 days for all months
            ),
            random.choice(["Bills", "Groceries", "Subscriptions", "Personal"]),
            round(random.uniform(10, 500), 2),
            faker.sentence(nb_words=5),
            random.choice(["Cash", "Online"]),
            round(random.uniform(0, 50), 2)
        ))
    return data


def insert_expenses_to_table(conn, month_name, expenses):
    """Insert generated expenses into the table."""
    cursor = conn.cursor()
    cursor.executemany(f"""
        INSERT INTO {month_name} (date, category, amount, description, payment_mode, cashback)
        VALUES (?, ?, ?, ?, ?, ?);
    """, expenses)
    conn.commit()

def list_tables():
    conn = sqlite3.connect(r"E:/GUVI/DS_Analyzing_Personal_Expenses/database/expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()  # Fetch all the results
    conn.close()
    return tables

print(list_tables())

def main():
    # Ensure the database folder exists
    os.makedirs("database", exist_ok=True)

    # Connect to SQLite database
    conn = sqlite3.connect(r"E:/GUVI/DS_Analyzing_Personal_Expenses/database/expenses.db")

    # Generate data for each month
    for month in range(1, 13):
        month_name = calendar.month_name[month]  # "January", "February", etc.
        create_table_for_month(conn, month_name)  # Create the table
        expenses = generate_monthly_expenses(month, 2025)  # Generate data
        insert_expenses_to_table(conn, month_name, expenses)  # Insert data
        print(f"Data for {month_name} added.")

    conn.close()


if __name__ == "__main__":
    main()
