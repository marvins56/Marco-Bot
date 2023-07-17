
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.agents import initialize_agent, AgentType
from langchain.document_loaders import TextLoader
from langchain.agents import tool
from langchain.text_splitter import CharacterTextSplitter
# ACTIVELOOP_TOKEN=os.getenv("ACTIVELOOP_TOKEN")
#
# def answer_with_deep_lake(query: str) -> str:
#
#     document_path="results/SqlJsonData.txt"
#     # Load environment variables
#     dotenv_path= find_dotenv()
#     load_dotenv(dotenv_path)
#
#     ACTIVELOOP_ORG=os.getenv("ACTIVELOOP_ORG")
#
#     # Instantiate embedding model
#     embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
#
#     # Create Deep Lake dataset
#     my_activeloop_org_id = ACTIVELOOP_ORG
#     my_activeloop_dataset_name = "langchain_course_from_zero_to_hero"
#     dataset_path = f"hub://{my_activeloop_org_id}/{my_activeloop_dataset_name}"
#     db = DeepLake(dataset_path=dataset_path, embedding_function=embeddings)
#
#     # Load and split the document
#     with open(document_path) as f:
#         chat_logs = f.read()
#     text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
#     pages = text_splitter.split_text(chat_logs)
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
#     texts = text_splitter.create_documents(pages)
#
#     # Add texts to database
#     db.add_texts(texts)
#
#     # Get the retriever object from the deep lake db object
#     retriever = db.as_retriever()
#
#     # Define some variables for the custom tool
#     CUSTOM_TOOL_N_DOCS = 10
#     CUSTOM_TOOL_DOCS_SEPARATOR ="\n\n"
#
#     @tool
#     def retrieve_n_docs_tool(query: str) -> str:
#         """ Searches for relevant documents that may contain the answer to the query."""
#         docs = retriever.get_relevant_documents(query)[:CUSTOM_TOOL_N_DOCS]
#         texts = [doc.page_content for doc in docs]
#         texts_merged = CUSTOM_TOOL_DOCS_SEPARATOR.join(texts)
#         return texts_merged
#
#     # Create an agent that uses the custom tool
#     llm = OpenAI(model="text-davinci-003", temperature=0)
#     agent = initialize_agent(
#         [retrieve_n_docs_tool],
#         llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
#     )
#
#     # Use the agent to answer the query
#     response = agent.run(query)
#
#     return response
#
# # document_path = "C:/Users/jukas/Desktop/Mackro/Marco-Bot/Marco/results/result_20230716_125005.txt"

from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import RetrievalQA
import os
from dotenv import find_dotenv, load_dotenv
from langchain.callbacks import StreamlitCallbackHandler
import streamlit as st

# Load environment variables
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

directory = 'results/'
def load_docs(directory):
    loader = DirectoryLoader(directory)
    documents = loader.load()
    return documents

def split_docs(documents,chunk_size=1000,chunk_overlap=20):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(documents)
    return docs
def RecommendationChain(query):

    documents = load_docs(directory)
    docs = split_docs(documents)
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma.from_documents(docs, embeddings)

    persist_directory = "chroma_db"

    vectordb = Chroma.from_documents(
        documents=docs, embedding=embeddings, persist_directory=persist_directory
    )

    vectordb.persist()

    model_name = "gpt-3.5-turbo"

    llm = ChatOpenAI(model_name=model_name,streaming=True)
    
    st_callback = StreamlitCallbackHandler(st.container())

    retrieval_chain = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=vectordb.as_retriever())
    result = retrieval_chain.run(query, callbacks=[st_callback])

    return result
