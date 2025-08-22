import streamlit as st
import sqlite3

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect("leave_management.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            paid_leaves_left INTEGER DEFAULT 12,
            sick_leaves_left INTEGER DEFAULT 12
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS leave_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            leave_type TEXT,
            days INTEGER,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY(employee_id) REFERENCES employees(id)
        )
    ''')
    conn.commit()
    return conn

# --- DB Helper Functions ---
def get_employees(conn):
    c = conn.cursor()
    c.execute("SELECT name, paid_leaves_left, sick_leaves_left FROM employees")
    return c.fetchall()

def get_leave_requests(conn):
    c = conn.cursor()
    c.execute("SELECT id, employee_id, leave_type, days, status FROM leave_requests")
    return c.fetchall()

# --- Main App ---
def main():
    st.title("🏢 Leave Management System (POC)")

    conn = init_db()

    # Section 1: Employee Records
    st.subheader("📋 Employee Records")
    employees = get_employees(conn)
    if employees:
        st.table(
            [{"Name": emp[0], "Paid Leaves Left": emp[1], "Sick Leaves Left": emp[2]} for emp in employees]
        )
    else:
        st.info("No employees found. Please add employees to view records.")

    st.markdown("---")  # separator line

    # Section 2: Leave Management
    st.subheader("📝 Leave Management")
    leave_requests = get_leave_requests(conn)
    if leave_requests:
        st.table(
            [
                {"Request ID": req[0], "Employee ID": req[1], "Leave Type": req[2], "Days": req[3], "Status": req[4]}
                for req in leave_requests
            ]
        )
    else:
        st.info("No leave requests yet.")

if __name__ == "__main__":
    main()
