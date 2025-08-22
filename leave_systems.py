import streamlit as st
import sqlite3
import pandas as pd
# --- Database setup ---
def init_db():
    conn = sqlite3.connect("leave_system.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            emp_id TEXT PRIMARY KEY,
            name TEXT,
            paid_leaves INTEGER DEFAULT 12,
            sick_leaves INTEGER DEFAULT 12
        )
    """)
    conn.commit()
    return conn

# --- Add Employee ---
def add_employee(conn, emp_id, name):
    conn.execute("""
        INSERT OR REPLACE INTO employees (emp_id, name, paid_leaves, sick_leaves)
        VALUES (?, ?, 12, 12)
    """, (emp_id, name))
    conn.commit()

# --- Apply Leave ---
def apply_leave(conn, emp_id, leave_type, days):
    cursor = conn.cursor()
    cursor.execute("SELECT paid_leaves, sick_leaves FROM employees WHERE emp_id = ?", (emp_id,))
    row = cursor.fetchone()

    if not row:
        return False, "Employee not found!"

    paid, sick = row

    if leave_type == "Paid Leave":
        if paid >= days:
            conn.execute("UPDATE employees SET paid_leaves = paid_leaves - ? WHERE emp_id = ?", (days, emp_id))
            conn.commit()
            return True, f"Leave approved! {days} Paid Leave deducted."
        else:
            return False, "Not enough Paid Leaves left."

    elif leave_type == "Sick Leave":
        if sick >= days:
            conn.execute("UPDATE employees SET sick_leaves = sick_leaves - ? WHERE emp_id = ?", (days, emp_id))
            conn.commit()
            return True, f"Leave approved! {days} Sick Leave deducted."
        else:
            return False, "Not enough Sick Leaves left."

    return False, "Invalid leave type."

# --- Get Employee Records ---
def get_employees(conn):
    return conn.execute("SELECT emp_id,name, paid_leaves, sick_leaves FROM employees").fetchall()

# --- Streamlit App ---
st.title("🏢 Leave Management System")

conn = init_db()

# Add employee section
st.subheader("➕ Add New Employee")
with st.form("add_emp_form"):
    emp_id = st.text_input("Employee ID")
    name = st.text_input("Employee Name")
    submit = st.form_submit_button("Add Employee")
    if submit and emp_id and name:
        add_employee(conn, emp_id, name)
        st.success(f"Employee {name} added successfully!")

# Apply leave section
st.subheader("📝 Apply Leave")
with st.form("leave_form"):
    emp_id_leave = st.text_input("Employee ID (for leave)")
    leave_type = st.selectbox("Leave Type", ["Paid Leave", "Sick Leave"])
    days = st.number_input("Number of Days", min_value=1, max_value=12)
    apply = st.form_submit_button("Apply Leave")
    if apply and emp_id_leave:
        success, msg = apply_leave(conn, emp_id_leave, leave_type, days)
        if success:
            st.success(msg)
        else:
            st.error(msg)

# Employee Records Table
st.subheader("📋 Employee Records")
employees = get_employees(conn)
df = pd.DataFrame(employees, columns=["emp_id","Name", "Paid Leaves Left", "Sick Leaves Left"])
if employees:
    st.table(df)
else:
    st.info("No employee records found yet.")
