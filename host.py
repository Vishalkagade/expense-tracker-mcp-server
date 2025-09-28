import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import calendar
import sqlite3

# Set page config
st.set_page_config(
    page_title="Monthly Expense Dashboard",
    page_icon="💰",
    layout="wide"
)

# Title and header
st.title("💰 Monthly Expense Dashboard")
st.markdown("---")

# Sidebar for date selection
st.sidebar.header("📅 Date Selection")
current_date = datetime.now()
selected_month = st.sidebar.selectbox(
    "Select Month",
    range(1, 13),
    index=current_date.month - 1,
    format_func=lambda x: calendar.month_name[x]
)
selected_year = st.sidebar.selectbox(
    "Select Year",
    range(2020, 2030),
    index=list(range(2020, 2030)).index(current_date.year)
)

# Connect to expenses.db database

# Function to get expenses from database
@st.cache_data
def get_expenses_from_db(month, year):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    
    # Query expenses for selected month and year
    cursor.execute("""
        SELECT category, SUM(amount) as total_amount
        FROM expenses 
        WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
        GROUP BY category
    """, (f"{month:02d}", str(year)))
    
    results = cursor.fetchall()
    conn.close()
    
    # Convert to dictionary
    expense_data = {category: amount for category, amount in results}
    
    # Return empty dict if no data found
    return expense_data if expense_data else {
        'No Data': 0.00
    }

# Get expense data for selected month and year
expense_data = get_expenses_from_db(selected_month, selected_year)

# Calculate total expenses
total_expenses = sum(expense_data.values())

# Main dashboard
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Monthly Expenses", f"${total_expenses:.2f}")

with col2:
    st.metric("Number of Categories", len(expense_data))

with col3:
    largest_category = max(expense_data, key=expense_data.get)
    st.metric("Largest Category", f"{largest_category} (${expense_data[largest_category]:.2f})")

st.markdown("---")

# Create two columns for charts
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📊 Expenses by Category - Pie Chart")
    
    # Create pie chart
    fig_pie = px.pie(
        values=list(expense_data.values()),
        names=list(expense_data.keys()),
        title="Monthly Expense Distribution",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

with chart_col2:
    st.subheader("📈 Expenses by Category - Bar Chart")
    
    # Create bar chart
    df = pd.DataFrame(
        list(expense_data.items()),
        columns=['Category', 'Amount']
    )
    df = df.sort_values('Amount', ascending=True)
    
    fig_bar = px.bar(
        df,
        x='Amount',
        y='Category',
        orientation='h',
        title="Monthly Expenses by Category",
        color='Amount',
        color_continuous_scale='viridis'
    )
    fig_bar.update_layout(showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

# Detailed breakdown table
st.markdown("---")
st.subheader("📋 Detailed Breakdown")

# Create a detailed dataframe
detailed_df = pd.DataFrame([
    {'Category': category, 'Amount': f"${amount:.2f}", 'Percentage': f"{(amount/total_expenses)*100:.1f}%"}
    for category, amount in sorted(expense_data.items(), key=lambda x: x[1], reverse=True)
])

st.dataframe(detailed_df, use_container_width=True, hide_index=True)

# Budget comparison section
st.markdown("---")
st.subheader("🎯 Budget Analysis")

budget_limit = st.number_input("Set Monthly Budget Limit", min_value=0.0, value=500.0, step=10.0)

if budget_limit > 0:
    remaining_budget = budget_limit - total_expenses
    budget_usage_pct = (total_expenses / budget_limit) * 100
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Budget Limit", f"${budget_limit:.2f}")
    
    with col2:
        color = "normal" if remaining_budget >= 0 else "inverse"
        st.metric("Remaining Budget", f"${remaining_budget:.2f}", delta=None)
    
    with col3:
        st.metric("Budget Used", f"{budget_usage_pct:.1f}%")
    
    # Budget progress bar
    progress_color = "🟢" if budget_usage_pct <= 80 else "🟡" if budget_usage_pct <= 100 else "🔴"
    st.write(f"{progress_color} Budget Usage Progress:")
    st.progress(min(budget_usage_pct / 100, 1.0))
    
    if remaining_budget < 0:
        st.error(f"⚠️ You have exceeded your budget by ${abs(remaining_budget):.2f}!")
    elif budget_usage_pct > 80:
        st.warning("⚠️ You have used more than 80% of your budget!")
    else:
        st.success("✅ You are within your budget limits!")

# Footer
st.markdown("---")
st.markdown("*Dashboard created with Streamlit. Data updates in real-time.*")

