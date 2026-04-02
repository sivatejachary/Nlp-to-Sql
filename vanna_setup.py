import os
from dotenv import load_dotenv

load_dotenv()

from vanna import Agent, AgentConfig
from vanna.core.registry import ToolRegistry
from vanna.core.user import UserResolver, User, RequestContext
from vanna.integrations.google import GeminiLlmService
from vanna.integrations.sqlite import SqliteRunner
from vanna.integrations.local.agent_memory import DemoAgentMemory

from vanna.tools import RunSqlTool
from vanna.tools.agent_memory import (
    SaveQuestionToolArgsTool,
    SearchSavedCorrectToolUsesTool
)

DB_PATH = "clinic.db"


# 🔹 Default user
class DefaultUserResolver(UserResolver):
    async def resolve_user(self, request_context: RequestContext) -> User:
        return User(
            id="default@user",
            email="default@user",
            group_memberships=["user", "admin"]
        )


def build_agent():

    #  1. Gemini LLM
    llm = GeminiLlmService(
        api_key=os.getenv("GOOGLE_API_KEY"),
        model="gemini-2.5-flash"
    )

    # 2. Database runner
    runner = SqliteRunner(database_path=DB_PATH)

    # 3. Tool registry
    tools = ToolRegistry()

    tools.register_local_tool(
        RunSqlTool(runner),
        access_groups=["user", "admin"]
    )

    tools.register_local_tool(
        SaveQuestionToolArgsTool(),
        access_groups=["admin"]
    )

    tools.register_local_tool(
        SearchSavedCorrectToolUsesTool(),
        access_groups=["user", "admin"]
    )

    #  4. Memory
    memory = DemoAgentMemory()

    #  5. STRONG SYSTEM PROMPT
    system_prompt = """
You are a strict SQL generator for a clinic database.

DATABASE SCHEMA:
patients(id, first_name, last_name, email, phone, date_of_birth, gender, city, registered_date)
doctors(id, name, specialization, department, phone)
appointments(id, patient_id, doctor_id, appointment_date, status, notes)
treatments(id, appointment_id, treatment_name, cost, duration_minutes)
invoices(id, patient_id, invoice_date, total_amount, paid_amount, status)

 CRITICAL RULES (MUST FOLLOW):
- You MUST ALWAYS call the tool "run_sql"
- You MUST ALWAYS return SQL
- You are NOT allowed to return plain text
- If you return text, it is WRONG

 STRICT BEHAVIOR:
- Convert question → SQL
- Call run_sql tool with SQL
- DO NOT explain anything
- DO NOT summarize results

SQL RULES:
- Use SQLite syntax
- Only SELECT queries allowed
- Use JOIN when needed
- Use GROUP BY for aggregation
- Use ORDER BY when needed

DATE RULES:
- Use strftime('%Y-%m', appointment_date) for monthly grouping
- Use date('now', '-6 months') for last 6 months
- Always use correct date filtering

EXAMPLE:

User: Show monthly appointment count for the past 6 months

SQL:
SELECT strftime('%Y-%m', appointment_date) AS month,
       COUNT(*) AS total_appointments
FROM appointments
WHERE appointment_date >= date('now', '-6 months')
GROUP BY month
ORDER BY month;

 FINAL RULE:
- NEVER return text
- ALWAYS call run_sql
"""

    #  6. Create Agent
    agent = Agent(
        llm_service=llm,
        tool_registry=tools,
        user_resolver=DefaultUserResolver(),
        agent_memory=memory,
        config=AgentConfig(system_prompt=system_prompt)
    )

    return agent, memory
