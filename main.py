from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import os
import re
from sql_validator import validate_sql
from google import genai

app = FastAPI()

class Query(BaseModel):
    question: str


# 🔹 run SQL
def run_sql(sql):
    conn = sqlite3.connect("clinic.db", check_same_thread=False)
    cur = conn.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows


# 🔥 generate SQL using Gemini (RELIABLE)
def generate_sql(question):
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    schema = """
    Tables:
    patients(id, first_name, last_name, email, phone, date_of_birth, gender, city, registered_date)
    doctors(id, name, specialization, department, phone)
    appointments(id, patient_id, doctor_id, appointment_date, status, notes)
    treatments(id, appointment_id, treatment_name, cost, duration_minutes)
    invoices(id, patient_id, invoice_date, total_amount, paid_amount, status)
    """

    prompt = f"""
    Convert this question into SQL.

    Rules:
    - Only return SQL
    - No explanation
    - Use SQLite syntax

    {schema}

    Question: {question}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

# remove code blocks ```sql ```
    text = re.sub(r"```sql|```", "", text, flags=re.IGNORECASE).strip()

# extract only SELECT query
    match = re.search(r"(SELECT .*?)(;|$)", text, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()

    return text


@app.post("/chat")
async def chat(req: Query):
    try:
        # ✅ generate SQL
        sql = generate_sql(req.question)

        # ✅ validate
        sql = validate_sql(sql)

        # ✅ execute
        rows = run_sql(sql)

        return {
            "sql": sql,
            "rows": rows
        }

    except Exception as e:
        return {"error": str(e)}


@app.get("/health")
def health():
    return {"status": "ok"}