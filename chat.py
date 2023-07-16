import streamlit as st
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.sql_database import SQLDatabase, SQLDatabaseChain
from dotenv import find_dotenv, load_dotenv
import os

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

def MultiChainRunner(query):
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
    search = SerpAPIWrapper()
    db = SQLDatabase.from_uri("mysql+mysqlconnector://root:password@localhost/macrol")
    db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="useful for when you need to answer questions about current events that are not in the database.\
            in case of retriving events they should be retrived in this format.\
            Event Name: Music Festival XYZ \
            Description: Join us for a weekend filled with live music performances from various artists.\
            Start Time: Saturday, July 17th, 2023, 6:00 PM\
            End Time: Sunday, July 18th, 2023, 11:00 PM\
            Location: City Park\
            Number of Upvotes: 50 \
            Sharable Link: https://musicfestivalxyz.com\
            other wise give a summary "
           
        ),
        Tool(
            name="Macro-DB",
            func=db_chain.run,
            description="useful for when you need to answer questions about events in the database.\
            in case of retriving events they should be retrived in this format.\
            Event Name: Music Festival XYZ \
            Description: Join us for a weekend filled with live music performances from various artists.\
            Start Time: Saturday, July 17th, 2023, 6:00 PM \
            End Time: Sunday, July 18th, 2023, 11:00 PM \
            Location: City Park \
            Number of Upvotes: 50 \
            Sharable Link: https://musicfestivalxyz.com\
            Input should be in the form of a question containing full context"
            
        )
    ]

    agent = initialize_agent(
        tools, 
        llm, 
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True
    )
    
    response = agent.run(query)
    return response

if __name__ == "__main__":
    st.title("Chatbot")

    user_input = st.text_input("Type your message:")

    if st.button("Send"):
        response = run_agent(user_input)
        st.text_area("Bot Response:", value=response, height=200)

