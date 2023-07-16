import os
import re
from pprint import pprint
from langchain.tools import Tool
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from dotenv import find_dotenv, load_dotenv
import streamlit as st


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID=os.getenv("GOOGLE_CSE_ID")
# Initialize the Google Search tool
search = GoogleSearchAPIWrapper()

def top5_results(query):
    return search.results(query, 3)

# Define the Google Search tool as a LangChain tool
search_tool = Tool(
    name="Google Search Snippets",
    description="Search Google for recent results.",
    func=top5_results
)

# Initialize the ChatOpenAI language model
llm = ChatOpenAI(temperature=0.5)

# Create the agent with the Google Search tool and ChatOpenAI language model
agent = initialize_agent(
    [search_tool],
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

   
query = "give me 3 evets present this week"
agent.run("return a list of leisure  events that have not expired and  match the description in the format of  event name ,description ,loacation ,number of upvotes ,sharable link : in  2023 from today onwards. here is my question : {query}")
   
