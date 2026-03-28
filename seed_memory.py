async def seed():
    agent, memory = build_agent()

    ctx = RequestContext(cookies={}, headers={})
    user = User(
        id="default@user",
        email="default@user",
        group_memberships=["user", "admin"]
    )

    qa_pairs = [
        ("How many patients?", "SELECT COUNT(*) FROM patients"),
        ("How many doctors?", "SELECT COUNT(*) FROM doctors"),
        ("Total appointments?", "SELECT COUNT(*) FROM appointments"),
        ("List all patients", "SELECT * FROM patients LIMIT 10"),
        ("List all doctors", "SELECT * FROM doctors LIMIT 10"),
        ("Total invoices?", "SELECT COUNT(*) FROM invoices"),
        ("Total treatments?", "SELECT COUNT(*) FROM treatments"),
        ("Show recent appointments", "SELECT * FROM appointments ORDER BY date DESC LIMIT 5"),
        ("Patients above age 50", "SELECT * FROM patients WHERE age > 50"),
        ("Doctors by specialization", "SELECT specialization, COUNT(*) FROM doctors GROUP BY specialization"),
        ("Appointments today", "SELECT * FROM appointments WHERE date = DATE('now')"),
        ("Total revenue", "SELECT SUM(amount) FROM invoices"),
        ("Top 5 expensive treatments", "SELECT * FROM treatments ORDER BY cost DESC LIMIT 5"),
        ("Patients count by gender", "SELECT gender, COUNT(*) FROM patients GROUP BY gender"),
        ("Doctors list", "SELECT name FROM doctors")
    ]

    for q, sql in qa_pairs:
        await memory.save_tool_usage(
            context=(ctx, user),
            question=q,
            tool_name="run_sql",
            args={"sql": sql}
        )

    print("Memory seeded with 15 Q&A pairs ✅")