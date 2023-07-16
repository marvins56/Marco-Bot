from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
import os
from dotenv import find_dotenv, load_dotenv
from langchain.prompts.prompt import PromptTemplate

import mysql.connector
dotenv_path= find_dotenv()
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

db = SQLDatabase.from_uri("mysql+mysqlconnector://root:password@localhost/macrol")
# llm = OpenAI(temperature=0, verbose=True)

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
db_chain = SQLDatabaseChain.from_llm(llm, db,  verbose=True, use_query_checker=True, return_intermediate_steps=True,top_k=3)
result = db_chain._run("how may events happened last week")

print(result)
