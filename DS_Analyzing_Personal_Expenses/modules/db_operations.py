import sqlite3
import pandas as pd

def fetch_data(query):
    try:
        conn = sqlite3.connect(r"E:/GUVI/DS_Analyzing_Personal_Expenses/database/expenses.db")
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
