import os
import sqlite3

# Ensure database folder exists
if not os.path.exists("database"):
    os.makedirs("database")


# Create table
def create_table():
    conn = sqlite3.connect("database/patients.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            contact TEXT,
            address TEXT
        )
        """
    )

    conn.commit()
    conn.close()


# Insert patient data
def insert_patient(name, age, gender, contact, address):
    conn = sqlite3.connect("database/patients.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO patients (name, age, gender, contact, address)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name, age, gender, contact, address),
    )

    conn.commit()
    conn.close()


# (Optional) Fetch all patients (useful later)
def get_all_patients():
    conn = sqlite3.connect("database/patients.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients")
    data = cursor.fetchall()

    conn.close()
    return data
