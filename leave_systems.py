import streamlit as st
import sqlite3
import pandas as pd

# Database setup
conn = sqlite3.connect("leave_mgmt.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS employees (
    name TEXT PRIMARY KEY,
    paid_leaves_left INTEGER,
    sick_leaves_left INTEGER
)
""")
conn.commit()

# Utility functions
def add_employee(name):
    c.execute("INSERT OR IGNORE INTO employees VALUES (?, ?, ?)", (name, 12, 12))
    conn.commit()

def get_employees():
    c.execute("SELECT name, paid_leaves_left, sick_leaves_left FROM employees")
    return c.fetchall()

def apply_leave(name, leave_type, days):
    if leave_type == "Paid Leave":
        c.execute("UPDATE employees SET paid_leaves_left = paid_leaves_left - ? WHERE name = ?", (days, name))
    elif leave_type == "Sick Leave":
        c.execute("UPDATE employees SET sick_leaves_left = sick_leaves_left - ? WHERE name = ?", (days, name))
    conn.commit()

# Layout
st.markdown(
    """
    <style>
    .title-left {
        text-align: left;
        font-size: 2em;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Use custom title
st.markdown('<p class="title-left">🏢 Employee Leave Management System</p>', unsafe_allow_html=True)


left_col, right_col = st.columns(2)

# Left Column
with left_col:
    st.subheader("➕ Add Employee")
    emp_name = st.text_input("Employee Name")
    if st.button("Add"):
        if emp_name.strip() != "":
            add_employee(emp_name.strip())
            st.success(f"Employee {emp_name} added!")
        else:
            st.warning("Enter a valid name")

    st.subheader("📋 Employee Records")
    employees = get_employees()
    if employees:
        df = pd.DataFrame(employees, columns=["Name", "Paid Leaves Left", "Sick Leaves Left"])
        st.table(df)

# Right Column
with right_col:
    st.subheader("📝 Apply for Leave")
    employees = get_employees()
    if employees:
        emp_list = [emp[0] for emp in employees]
        selected_emp = st.selectbox("Select Employee", emp_list)
        leave_type = st.selectbox("Leave Type", ["Paid Leave", "Sick Leave"])
        days = st.number_input("No. of Days", min_value=1, max_value=12, step=1)
        if st.button("Apply Leave"):
            apply_leave(selected_emp, leave_type, days)
            st.success(f"{days} {leave_type}(s) applied for {selected_emp}")

    st.subheader("📊 Leave Balance")
    employees = get_employees()
    if employees:
        df = pd.DataFrame(employees, columns=["Name", "Paid Leaves Left", "Sick Leaves Left"])
        st.table(df)
