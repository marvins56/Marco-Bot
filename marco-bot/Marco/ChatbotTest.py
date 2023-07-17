

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

from tools import CustomEventCreator

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")


def MultiChainRunner(query):
    try:
        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
        search = SerpAPIWrapper()
        db = SQLDatabase.from_uri("mysql+mysqlconnector://root:password@localhost/macrol")
        db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
        
        EventCreatorTool = CustomEventCreator()

        tools = [
            Tool(
                name="Search",
                func=search.run,
                description="Useful for answering questions about current events not in the database. they MUST include links\
                        incase you are returning events use this format \
                        Event Name: Art Exhibition ABC\
                        Description: Explore a diverse collection of artworks from local and international artists.\
                        Start Time: Friday, July 23rd, 2023, 10:00 AM\
                        End Time: Sunday, July 25th, 2023, 6:00 PM\
                        Location: Art Gallery XYZ\
                        Number of Upvotes: 30\
                        bookingLink: https://artexhibitionabc.com "
            ),
            Tool(
                name="Macro-DB",
                func=db_chain.run,
                description="Useful for answering questions about events in the database. they MUST include link \
                incase you are returning events use this format \
                Event Name: Art Exhibition ABC\
                Description: Explore a diverse collection of artworks from local and international artists.\
                Start Time: Friday, July 23rd, 2023, 10:00 AM\
                End Time: Sunday, July 25th, 2023, 6:00 PM\
                Location: Art Gallery XYZ\
                Number of Upvotes: 30\
                bookingLink: https://artexhibitionabc.com\
                other wise use lists and descriptions for the requested items."
            ),
            EventCreatorTool,
            
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
    
def create_folder():
    """Creates the necessary directories for storing the conversation data."""
    directory = 'conversations'
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_conversation(conversation):
    """Saves the conversation into a text file."""
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f'conversations/{today_date}.txt'
    with open(filename, "a") as file:
        for message in conversation:
            file.write(f"{message['role']}\n{message['time']}\n{message['text']}\n\n")

def load_conversation():
    """Loads the conversation from a text file if it's not empty."""
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

def create_event(name, description, start_date, end_date,Event_start_time,Event_end_time, location, image, price,category, link):
    # Process the event details and perform the necessary actions
    event_details = {
        "Event Name": name,
        "Description": description,
        "Start Date": start_date,
        "End date": end_date,
        "Event_start_time": Event_start_time,
        "Event_end_time,": Event_end_time,
        "Location": location,
        
        "Image": image,
        "price":price,
        "Event Category": category,
        "Link": link
    }
    # Perform the desired actions with the event details
    return event_details
    # print("Event created:", event_details)

# def app():
#     st.title("Chatbot")

#     user_input = st.text_input("Type your message:")
#     # event_input = st.text_input("Ask about an event:") if st.button("Ask about events") else None

#     create_folder()
#     conversation = load_conversation()

#     if st.button("Send"):
#         try:
#             result = MultiChainRunner(user_input)
#             current_time = datetime.datetime.now().strftime("%H:%M:%S")
#             conversation.append({
#                 "role": "User",
#                 "time": current_time,
#                 "text": user_input
#             })
#             conversation.append({
#                 "role": "Bot",
#                 "time": current_time,
#                 "text": str(result)
#             })
#             save_conversation(conversation)
#         except Exception as e:
#             st.error(f"An error occurred: {str(e)}")
    
#     with st.form("create_event_form"):
#         if st.button("Create Event"):
#             name = st.text_input("Event Name")
#             description = st.text_area("Description")
#             start_date = st.date_input("Start Date", value=datetime.date.today())
#             start_date = start_date.strftime("%Y-%m-%d")
#             end_date = st.date_input("End Date", value=datetime.date.today())
#             end_date = end_date.strftime("%Y-%m-%d")

#             Event_start_time = st.time_input("Start Time")
#             Event_end_time = st.time_input("End Time")
#             location = st.text_input("Location")
            
#             image = st.file_uploader("Image")
#             is_free = st.radio("Price", options=["Free", "PAID"])
#             if is_free == "PAID":
#                 price = st.number_input("Price")
#             else:
#                 price = None
#             category = st.text_input("Event Category")
#             link = st.text_input("Link")
#             create_button = st.form_submit_button("Create")
    
#     if create_button:
#         try:
#             EventDetails = create_event(name, description, start_date, end_date,Event_start_time,Event_end_time, location, image,price, category, link)
#             result = MultiChainRunner(EventDetails)
#             st.success("Event created successfully!")
#         except Exception as e:
#             st.error(f"An error occurred: {str(e)}")
                
               
    
#     for message in conversation:
#         if message['role'] == 'User':
#   
#           st.markdown(f"<div style='text-align: right; color: blue;'>**{message['role']} ({message['time']}):** {message['text']}</div>", unsafe_allow_html=True)
def app():
    st.title("Chatbot")

    user_input = st.text_input("Type your message:")
    # event_input = st.text_input("Ask about an event:") if st.button("Ask about events") else None

    create_folder()
    conversation = load_conversation()

    if st.button("Send"):
        try:
            result = MultiChainRunner(user_input)
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            conversation.append({
                "role": "User",
                "time": current_time,
                "text": user_input
            })
            conversation.append({
                "role": "Bot",
                "time": current_time,
                "text": str(result)
            })
            save_conversation(conversation)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    if st.button("Create Event"):
        with st.form("create_event_form"):
            name = st.text_input("Event Name")
            description = st.text_area("Description")
            start_date = st.date_input("Start Date", value=datetime.date.today())
            start_date = start_date.strftime("%Y-%m-%d")
            end_date = st.date_input("End Date", value=datetime.date.today())
            end_date = end_date.strftime("%Y-%m-%d")

            Event_start_time = st.time_input("Start Time")
            Event_end_time = st.time_input("End Time")
            location = st.text_input("Location")
            
            image = st.file_uploader("Image")
            is_free = st.checkbox("Free")
            if not is_free:
                price = st.number_input("Price",key="price_input")
            
            category = st.text_input("Event Category")
            link = st.text_input("Link")
            create_button = st.form_submit_button("Create")
    
            if create_button:
                try:
                    EventDetails = create_event(name, description, start_date, end_date, Event_start_time, Event_end_time, location, image, price, category, link)
                    result = MultiChainRunner(EventDetails)
                    st.success("Event created successfully!")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                
    
    for message in conversation:
        if message['role'] == 'User':
            st.markdown(f"<div style='text-align: right; color: blue;'>**{message['role']} ({message['time']}):** {message['text']}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    app()


# def app():
#     st.title("Chatbot")

#     user_input = st.text_input("Type your message:")
#     # event_input = st.text_input("Ask about an event:") if st.button("Ask about events") else None
#     progress_bar = st.progress(0)
#     create_folder()
#     conversation = load_conversation()

#     if st.button("Send"):
#         try:
#             result = MultiChainRunner(user_input)
#             # Update the progress bar to indicate completion
#             progress_bar.progress(1.0)
#             current_time = datetime.datetime.now().strftime("%H:%M:%S")
#             conversation.append({
#                 "role": "User",
#                 "time": current_time,
#                 "text": user_input
#             })
#             conversation.append({
#                 "role": "Bot",
#                 "time": current_time,
#                 "text": str(result)
#             })
#             save_conversation(conversation)
#         except Exception as e:
#             st.error(f"An error occurred: {str(e)}")
       
    
#     for message in conversation:
#         if message['role'] == 'User':
#             st.markdown(f"<div style='text-align: right; color: blue;'>**{message['role']} ({message['time']}):** {message['text']}</div>", unsafe_allow_html=True)
#         else:
#             st.markdown(f"<div style='text-align: left; color: white;'>**{message['role']} ({message['time']}):** {message['text']}</div>", unsafe_allow_html=True)
     
   