from typing import Optional, Type
from dotenv import find_dotenv, load_dotenv
import os
from langchain import OpenAI, SQLDatabase
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool, StructuredTool, Tool, tool
from langchain.callbacks import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(temperature=0)


class CustomEventCreator(BaseTool):
    name = "EventCreator"
    description = "useful for when you need to create event."

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        db = SQLDatabase.from_uri("mysql+mysqlconnector://root:password@localhost/macrol")
        toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=0))
        agent_executor = create_sql_agent(
        llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS
        )

        return agent_executor.run(query)
    
    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("tool does not support async")

