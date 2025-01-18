import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


# Example function for plotting monthly trends
def plot_monthly_trends(data):
    """Plot spending trends over time."""
    data["date"] = pd.to_datetime(data["date"])  # Ensure 'date' is datetime
    monthly_data = data.groupby(data["date"].dt.to_period("M"))["amount"].sum()

    # Plotting
    fig, ax = plt.subplots()
    monthly_data.plot(kind="line", ax=ax, title="Monthly Spending Trends")
    st.pyplot(fig)


# Function for top categories plot
def plot_top_categories(data):
    """Plot the top spending categories."""
    top_categories = data.groupby("category")["amount"].sum().sort_values(ascending=False).head(5)

    # Plotting
    fig, ax = plt.subplots()
    top_categories.plot(kind="bar", ax=ax, title="Top 5 Spending Categories")
    st.pyplot(fig)
