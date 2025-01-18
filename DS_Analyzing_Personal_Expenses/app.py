import streamlit as st
import sqlite3
import pandas as pd
import calendar
from modules.db_operations import fetch_data
from modules.eda import plot_monthly_trends, plot_top_categories

# Title of the app
st.title("Personal Expense Tracker")

# Sidebar for Month Selection
month = st.sidebar.selectbox("Select a Month", [calendar.month_name[i] for i in range(1, 13)])

# Display Total Spending by Category for the Selected Month
st.header(f"Total Spending by Category in {month}")

# Construct the SQL query
query = f"""
SELECT category, SUM(amount) AS total_spent
FROM `{month}`  # Table name with the month name
GROUP BY category;
"""

# Debug: print the query being executed
st.write(f"Executing query: {query}")

try:
    # Fetch data
    df = fetch_data(query)
    if df is not None and not df.empty:
        # Display the DataFrame
        st.write(df)

        # Pie Chart for Spending Distribution by Category
        st.subheader(f"Spending Distribution in {month}")
        st.write("Pie chart for spending distribution by category.")
        st.pie_chart(df.set_index('category')['total_spent'])
    else:
        st.warning("No data found for the selected month.")

except Exception as e:
    st.error(f"Error fetching data: {e}")

# Monthly Spending Trends (Line Chart)
st.subheader(f"Monthly Spending Trends in {month}")
query_trends = f"""
SELECT strftime('%Y-%m', date) AS month, SUM(amount) AS total_spent
FROM `{month}`
GROUP BY month;
"""

try:
    df_trends = fetch_data(query_trends)
    if df_trends is not None and not df_trends.empty:
        st.line_chart(df_trends.set_index('month')['total_spent'])
    else:
        st.warning("No trend data found for the selected month.")
except Exception as e:
    st.error(f"Error fetching trend data: {e}")

# Top 5 Categories by Spending (Bar Chart)
st.subheader(f"Top 5 Categories by Spending in {month}")
query_top_categories = f"""
SELECT category, SUM(amount) AS total_spent
FROM `{month}`
GROUP BY category
ORDER BY total_spent DESC
LIMIT 5;
"""

try:
    df_top_categories = fetch_data(query_top_categories)
    if df_top_categories is not None and not df_top_categories.empty:
        st.bar_chart(df_top_categories.set_index('category')['total_spent'])
    else:
        st.warning("No top categories data found for the selected month.")
except Exception as e:
    st.error(f"Error fetching top categories data: {e}")

# Checkbox to display cashback data
show_cashback = st.checkbox("Show Cashback Data")
if show_cashback:
    query_cashback = f"""
    SELECT SUM(cashback) AS total_cashback
    FROM `{month}`
    """

    try:
        df_cashback = fetch_data(query_cashback)
        if df_cashback is not None and not df_cashback.empty:
            st.write(f"Total cashback in {month}: {df_cashback['total_cashback'].iloc[0]}")
        else:
            st.warning("No cashback data found for the selected month.")
    except Exception as e:
        st.error(f"Error fetching cashback data: {e}")
