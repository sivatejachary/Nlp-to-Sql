import os
from dotenv import load_dotenv

load_dotenv()

from vanna import Agent, AgentConfig
from vanna.core.registry import ToolRegistry
from vanna.core.user import UserResolver, User, RequestContext
from vanna.integrations.google import GeminiLlmService
from vanna.integrations.sqlite import SqliteRunner
from vanna.integrations.local.agent_memory import DemoAgentMemory

from vanna.tools import RunSqlTool, VisualizeDataTool
from vanna.tools.agent_memory import (
    SaveQuestionToolArgsTool,
    SearchSavedCorrectToolUsesTool
)

DB_PATH = "clinic.db"

# ✅ REQUIRED in Vanna 2.0
class DefaultUserResolver(UserResolver):
    async def resolve_user(self, request_context: RequestContext) -> User:
        return User(
            id="default@user",
            email="default@user",
            group_memberships=["user", "admin"]
        )

def build_agent():
    llm = GeminiLlmService(
        api_key=os.getenv("GOOGLE_API_KEY"),
        model="gemini-2.5-flash"
    )

    runner = SqliteRunner(database_path=DB_PATH)

    tools = ToolRegistry()

    tools.register_local_tool(
        RunSqlTool(runner),
        access_groups=["user", "admin"]
    )

    tools.register_local_tool(
        VisualizeDataTool(),
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

    memory = DemoAgentMemory()

    agent = Agent(
        llm_service=llm,
        tool_registry=tools,
        user_resolver=DefaultUserResolver(),   # ✅ FIX
        agent_memory=memory,
        config=AgentConfig()
    )
    

    return agent, memory