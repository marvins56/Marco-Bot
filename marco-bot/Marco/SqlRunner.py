import streamlit as st
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
import os
from dotenv import find_dotenv, load_dotenv
import mysql.connector
dotenv_path= find_dotenv()
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

db = SQLDatabase.from_uri("mysql+mysqlconnector://root:password@localhost/macrol")
# # 
# toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=0))

# # agent_executor = create_sql_agent(
# #     llm=OpenAI(temperature=0),
# #     toolkit=toolkit,
# #     verbose=True,
# #     agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
# # )

# agent_executor = create_sql_agent(
#     llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
#     toolkit=toolkit,
#     verbose=True,
#     agent_type=AgentType.OPENAI_FUNCTIONS
# )


# response = agent_executor.run("event that happened this week")
# print(response)
# # def main():
# #     st.title("SQL Chatbot")
# #     user_input = st.text_input("Type your message:")
# #     if st.button("Send"):
# #         response = agent_executor.run(user_input)
# #         st.write(f"Bot: {response}")


# # if __name__ == "__main__":
# #     main()
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.prompts.prompt import PromptTemplate


def get_sql_result(question: str):
    try:
        _DEFAULT_TEMPLATE = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
        Use the following format:

        Question: "Question here"
        SQLQuery: "SQL Query to run"
        SQLResult: "Result of the SQLQuery"
        Answer: "Final answer here"

        Only use the following tables:

        {table_info}

        If someone asks for the table foobar, they really mean the employee table.

        Question: {input}"""
        
        PROMPT = PromptTemplate(
            input_variables=["input", "table_info", "dialect"], template=_DEFAULT_TEMPLATE
        )

        llm = OpenAI(temperature=0,model="gpt-3.5-turbo")

        # The database initialization is not provided in your original code
        # Replace the `...` with appropriate arguments to instantiate the SQLDatabase
        db = SQLDatabase.from_uri("mysql+mysqlconnector://root:password@localhost/macrol")

        db_chain = SQLDatabaseChain.from_llm(llm, db, prompt=PROMPT, use_query_checker=True,verbose=True)

        result = db_chain.run(question)

        return result

    except Exception as e:
        print(f"An error occurred: {e}")
        
# # Usage
# question = "what events happened yesterday"
#
# (get_sql_result(question))


