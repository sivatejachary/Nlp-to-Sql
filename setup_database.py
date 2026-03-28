import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = "clinic.db"

first_names = ["Ravi","Amit","Priya","Sneha","Kiran","Anjali","Rahul","Pooja","Vikram","Neha"]
last_names = ["Reddy","Sharma","Kumar","Patel","Singh","Gupta","Nair","Das","Yadav","Mehta"]
cities = ["Hyderabad","Bangalore","Chennai","Mumbai","Delhi","Pune","Kolkata","Jaipur"]
specializations = ["Dermatology","Cardiology","Orthopedics","General","Pediatrics"]
statuses = ["Scheduled","Completed","Cancelled","No-Show"]

def random_date():
    return datetime.now() - timedelta(days=random.randint(0, 365))


def create_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 🔥 Drop old tables
    cur.executescript("""
    DROP TABLE IF EXISTS patients;
    DROP TABLE IF EXISTS doctors;
    DROP TABLE IF EXISTS appointments;
    DROP TABLE IF EXISTS treatments;
    DROP TABLE IF EXISTS invoices;
    """)

    # 🔥 Create tables
    cur.executescript("""
    CREATE TABLE patients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        phone TEXT,
        date_of_birth DATE,
        gender TEXT,
        city TEXT,
        registered_date DATE
    );

    CREATE TABLE doctors(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        specialization TEXT,
        department TEXT,
        phone TEXT
    );

    CREATE TABLE appointments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_id INTEGER,
        appointment_date DATETIME,
        status TEXT,
        notes TEXT
    );

    CREATE TABLE treatments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        appointment_id INTEGER,
        treatment_name TEXT,
        cost REAL,
        duration_minutes INTEGER
    );

    CREATE TABLE invoices(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        invoice_date DATE,
        total_amount REAL,
        paid_amount REAL,
        status TEXT
    );
    """)

    # ---------------- PATIENTS ----------------
    for _ in range(200):
        cur.execute("""
        INSERT INTO patients VALUES (NULL,?,?,?,?,?,?,?,?)
        """, (
            random.choice(first_names),
            random.choice(last_names),
            None if random.random()<0.3 else f"user{random.randint(1,999)}@mail.com",
            None if random.random()<0.3 else f"9{random.randint(100000000,999999999)}",
            random_date().date(),
            random.choice(["M","F"]),
            random.choice(cities),
            random_date().date()
        ))

    # ---------------- DOCTORS ----------------
    for i in range(15):
        spec = specializations[i % 5]  # ensures all 5 types
        cur.execute("""
        INSERT INTO doctors VALUES (NULL,?,?,?,?)
        """, (
            "Dr. " + random.choice(first_names),
            spec,
            spec + " Dept",
            f"8{random.randint(100000000,999999999)}"
        ))

    # ---------------- APPOINTMENTS ----------------
    appointment_ids_completed = []

    for _ in range(500):
        patient_id = random.choices(
            population=range(1,201),
            weights=[random.randint(1,5) for _ in range(200)]
        )[0]

        doctor_id = random.choices(
            population=range(1,16),
            weights=[random.randint(1,5) for _ in range(15)]
        )[0]

        status = random.choice(statuses)

        cur.execute("""
        INSERT INTO appointments VALUES (NULL,?,?,?,?,?)
        """, (
            patient_id,
            doctor_id,
            random_date(),
            status,
            None if random.random()<0.3 else "Routine check"
        ))

        if status == "Completed":
            appointment_ids_completed.append(cur.lastrowid)

    # ---------------- TREATMENTS ----------------
    for _ in range(350):
        if not appointment_ids_completed:
            break

        cur.execute("""
        INSERT INTO treatments VALUES (NULL,?,?,?,?)
        """, (
            random.choice(appointment_ids_completed),
            random.choice(["X-Ray","Scan","Blood Test","Surgery","Consultation"]),
            random.randint(50,5000),
            random.randint(10,120)
        ))

    # ---------------- INVOICES ----------------
    for _ in range(300):
        total = random.randint(100,5000)
        paid = random.randint(0,total)

        if paid == total:
            status = "Paid"
        else:
            status = random.choice(["Pending","Overdue"])

        cur.execute("""
        INSERT INTO invoices VALUES (NULL,?,?,?,?,?)
        """, (
            random.randint(1,200),
            random_date().date(),
            total,
            paid,
            status
        ))

    conn.commit()
    conn.close()

    print("✅ Created 200 patients, 15 doctors, 500 appointments, 350 treatments, 300 invoices")


if __name__ == "__main__":
    create_db()