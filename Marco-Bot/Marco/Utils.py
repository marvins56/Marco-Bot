import os
import datetime
import mysql.connector
import uuid


from openai import ChatCompletion
import streamlit as st
from langchain import LLMChain, OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.prompts.prompt import PromptTemplate
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from dotenv import find_dotenv, load_dotenv
import os

import mysql.connector
import datetime
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent, Tool

from langchain.prompts.prompt import PromptTemplate



from tools import CustomEventCreator

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")


# def MultiChainRunner(query):
#     try:
#         llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", max_tokens=3000)
#         search = SerpAPIWrapper()
        
#         EventCreatorTool = CustomEventCreator()

#         tools = [
#             # Tool(
#             #     name="Search",
#             #     func=search.run,
#             #     description="Useful for answering questions about current events not in the database. they MUST include links"
#             # ),
#             # Tool(
#             #     name="Macro-DB",
#             #     func=db_chain.run,
#             #     description="Useful for querying information about events and event categories in the database. "

#             # ),
#             # EventCreatorTool
            
#         ]

#         agent = initialize_agent(
#             tools, 
#             llm, 
#             agent=AgentType.OPENAI_FUNCTIONS,
#             verbose=True
#         )

#         response = agent.run(query)
#         print(response)
#         return response

#     except Exception as e:
#         return f"An error occurred: {str(e)}"
    


# MultiChainRunner("event that happened this week")

def MultiChainRunner(query):
    try:
        llm = OpenAI(temperature=0, model="gpt-3.5-turbo-0613",max_tokens_limit=4000)
        search = SerpAPIWrapper()
        db = SQLDatabase.from_uri("mysql+mysqlconnector://root:password@localhost/macrol")
        db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
        
        EventCreatorTool = CustomEventCreator()

        tools = [
            Tool(
                name="Search",
                func=search.run,
                description="Useful for answering questions about current events not in the database. they MUST include links"
            ),
            Tool(
                name="Macro-DB",
                func=db_chain.run,
                description="Useful for querying information about events and event categories in the database \
                To retrieve events, provide a link to the event. The format should be as follows:\
                Event Name: Art Exhibition ABC\
                Description: Explore a diverse collection of artworks from local and international artists.\
                Start Time: Friday, July 23rd, 2023, 10:00 AM\
                End Time: Sunday, July 25th, 2023, 6:00 PM\
                Location: Art Gallery XYZ\
                Number of Upvotes: 3\
                Booking Link: https://artexhibitionabc.com\
                For other queries, use lists and descriptions to provide the requested items."

            ),
            
            
        ]

        agent = initialize_agent(
            tools, 
            llm, 
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True
        )

        response = agent.run(query)
        return response

    except Exception as e:
        return f"An error occurred: {str(e)}"

        
UPLOAD_DIR = "Marco/"

def create_folder():
    # Function to create the necessary directories for storing the conversation data
    directory = 'conversations'
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_conversation(conversation):
    # Function to save the conversation into a text file
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f'conversations/{today_date}.txt'
    with open(filename, "a") as file:
        for message in conversation:
            file.write(f"{message['role']}\n{message['time']}\n{message['text']}\n\n")

def load_conversation():
    # Function to load the conversation from a text file
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f'conversations/{today_date}.txt'
    if os.path.exists(filename) and os.stat(filename).st_size > 0:
        with open(filename, "r") as file:
            data = file.read()
            convs = data.split('\n\n')[:-1]  # Remove the last empty item
            conversations = []
            for conv in convs:
                lines = conv.split('\n')
                if len(lines) == 3:
                    role, time, text = lines
                    conversations.append({
                        "role": role,
                        "time": time,
                        "text": text
                    })
            return conversations
    else:
        return []

def save_image(image, filename):
    # Function to save the uploaded image file
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    image_path = os.path.join(UPLOAD_DIR, filename)
    with open(image_path, 'wb') as file:
        file.write(image.read())
