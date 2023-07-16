from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

import os
from dotenv import find_dotenv, load_dotenv
import mysql.connector
dotenv_path= find_dotenv()
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

template = """You are a prompt engineer for an event management system.
Your role is to assist users with their event-related queries and provide relevant information.

As a prompt engineer, you have extensive knowledge about events, including event details, dates, locations, and more. You can use this knowledge to answer questions, provide event recommendations, and share event-specific information.
You will be working with an event management assistant 
The assistant can generate human-like responses based on the input it receives, allowing for natural-sounding conversations.
 

{history}
User: {user_input}
Assistant:"""

prompt = PromptTemplate(input_variables=["history", "user_input"], template=template)


event_assistant_chain = LLMChain(
    llm=OpenAI(temperature=0),
    prompt=prompt,
    verbose=True,
    memory=ConversationBufferWindowMemory(k=2),
)

output = event_assistant_chain.predict(
    user_input="What are some upcoming music concerts in my area?"
)
print(output)


