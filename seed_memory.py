import asyncio
from vanna_setup import build_agent
from vanna.core.user import User, RequestContext


async def seed():
    agent, memory = build_agent()

    ctx = RequestContext(cookies={}, headers={})
    user = User(
        id="default@user",
        email="default@user",
        group_memberships=["user", "admin"]
    )

    qa_pairs = [
        ("How many patients?",              "SELECT COUNT(*) FROM patients"),
        ("How many doctors?",               "SELECT COUNT(*) FROM doctors"),
        ("Total appointments?",             "SELECT COUNT(*) FROM appointments"),
        ("List all patients",               "SELECT * FROM patients LIMIT 10"),
        ("List all doctors",                "SELECT * FROM doctors LIMIT 10"),
        ("Total invoices?",                 "SELECT COUNT(*) FROM invoices"),
        ("Total treatments?",               "SELECT COUNT(*) FROM treatments"),
        ("Show recent appointments",        "SELECT * FROM appointments ORDER BY appointment_date DESC LIMIT 5"),
        ("Patients above age 50",           "SELECT * FROM patients WHERE (strftime('%Y', 'now') - strftime('%Y', date_of_birth)) > 50"),
        ("Doctors by specialization",       "SELECT specialization, COUNT(*) FROM doctors GROUP BY specialization"),
        ("Appointments today",              "SELECT * FROM appointments WHERE DATE(appointment_date) = DATE('now')"),
        ("Total revenue",                   "SELECT SUM(total_amount) FROM invoices"),
        ("Top 5 expensive treatments",      "SELECT * FROM treatments ORDER BY cost DESC LIMIT 5"),
        ("Patients count by gender",        "SELECT gender, COUNT(*) FROM patients GROUP BY gender"),
        ("Doctors list",                    "SELECT name FROM doctors"),
        ("Monthly appointment count past 6 months",
         "SELECT strftime('%Y-%m', appointment_date) AS month, COUNT(*) AS count "
         "FROM appointments "
         "WHERE appointment_date >= DATE('now', '-6 months') "
         "GROUP BY month ORDER BY month"),
    ]

    for q, sql in qa_pairs:
        await memory.save_tool_usage(
            context=(ctx, user),
            question=q,
            tool_name="run_sql",
            args={"sql": sql}
        )

    print(f" Memory seeded with {len(qa_pairs)} Q&A pairs")


if __name__ == "__main__":
    asyncio.run(seed())
