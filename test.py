import os
from dotenv import find_dotenv, load_dotenv
from langchain.agents.agent_types import AgentType

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from langchain.chains.router import MultiPromptChain
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain import HuggingFaceHub
from getpass import getpass

HUGGINGFACEHUB_API_TOKEN = getpass()
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

eventLists = """You are a very smart text formater . \

You are great at formating  content about events  in a concise and easy to understand manner without changing anything or making a meaning out of it. \
when given a bunch of data about evenst containing infomation of event name, description, start timme, end time loacation and sharable link and number of upvotes the event has.\
you organise them a list structure like. \

event name : 
description :
start time :
end time :
loacation :
number of upvotes :
sharable link :
whent that event has a description , make meaning out of it by adding a suggestive description with a lable, suggested description.
when you cannot organise the data return a summary of the data. 


Here is a query:
{input}"""


EvenDescriptions = """You are a very good event descriptor. You are great at answering  questions about event descriptions. \
You are so good because you are able to break down hard descriptiond small meaning full descriptions in a list, \


Here is a query:
{input}"""

prompt_infos = [
    {
        "name": "eventLists",
        "description": "Good for answering questions about physics",
        "prompt_template": eventLists,
    },
    {
        "name": "EvenDescriptions",
        "description": "Good for answering  questions about event descriptor",
        "prompt_template": EvenDescriptions,
    },
]

# repo_id = "tiiuae/falcon-40b"

# llm = HuggingFaceHub(
#     repo_id=repo_id, model_kwargs={"temperature": 0.5, "max_length": 64}
# )
llm= OpenAI()

destination_chains = {}
for p_info in prompt_infos:
    name = p_info["name"]
    prompt_template = p_info["prompt_template"]
    prompt = PromptTemplate(template=prompt_template, input_variables=["input"])
    chain = LLMChain(llm=llm, prompt=prompt)
    destination_chains[name] = chain

default_chain = ConversationChain(llm=llm, output_key="text")

# # LLMRouterChain
# This chain uses an LLM to determine how to route things.

destinations = [f"{p['name']}: {p['description']}" for p in prompt_infos]
destinations_str = "\n".join(destinations)
router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(destinations=destinations_str)
router_prompt = PromptTemplate(
    template=router_template,
    input_variables=["input"],
    output_parser=RouterOutputParser(),
)
router_chain = LLMRouterChain.from_llm(llm, router_prompt)

chain = MultiPromptChain(
    router_chain=router_chain,
    destination_chains=destination_chains,
    default_chain=default_chain,
    verbose=True,
)

db = SQLDatabase.from_uri("mysql+mysqlconnector://root:password@localhost/macrol")
# 
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)
user_input="what events are there nest week in s summarised list "
response = agent_executor.run(user_input)

# print(chain.run(response))