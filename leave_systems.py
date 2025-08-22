import streamlit as st
import sqlite3
import pandas as pd

# Database connection
def init_db():
    conn = sqlite3.connect("leave_management.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            paid_leaves INTEGER DEFAULT 12,
            sick_leaves INTEGER DEFAULT 12
        )
    """)
    conn.commit()
    return conn

# Add employee
def add_employee(conn, name):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO employees (name) VALUES (?)", (name,))
    conn.commit()

# Get employees
def get_employees(conn):
    return pd.read_sql("SELECT id, name FROM employees", conn)

# Get leave records
def get_leave_records(conn):
    return pd.read_sql("SELECT name, paid_leaves, sick_leaves FROM employees", conn)

# Deduct leave
def deduct_leave(conn, name, leave_type):
    cursor = conn.cursor()
    if leave_type == "Paid Leave":
        cursor.execute("UPDATE employees SET paid_leaves = paid_leaves - 1 WHERE name = ? AND paid_leaves > 0", (name,))
    else:
        cursor.execute("UPDATE employees SET sick_leaves = sick_leaves - 1 WHERE name = ? AND sick_leaves > 0", (name,))
    conn.commit()

# Streamlit App
st.title("🏢 Leave Management System")

conn = init_db()

# Sidebar - Add Employee
st.sidebar.header("➕ Add Employee")
new_name = st.sidebar.text_input("Employee Name")
if st.sidebar.button("Add"):
    if new_name.strip():
        add_employee(conn, new_name.strip())
        st.sidebar.success(f"Employee {new_name} added!")

# Leave Application Section
st.subheader("📝 Apply for Leave")
employees_df = get_employees(conn)
if not employees_df.empty:
    selected_emp = st.selectbox("Select Employee", employees_df["name"])
    leave_type = st.radio("Leave Type", ["Paid Leave", "Sick Leave"])
    if st.button("Apply Leave"):
        deduct_leave(conn, selected_emp, leave_type)
        st.success(f"{leave_type} applied for {selected_emp}!")
else:
    st.warning("No employees found. Please add an employee first.")

# Display Employee List
st.subheader("👥 Employee List")
emp_list = get_employees(conn)
st.table(emp_list)

# Display Leave Records
st.subheader("📋 Leave Records")
leave_records = get_leave_records(conn)
st.table(leave_records)
