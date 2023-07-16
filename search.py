# from langchain.vectorstores import Chroma
# import os
# from dotenv import find_dotenv, load_dotenv
# from langchain.document_loaders import DirectoryLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# import openai
# from langchain.embeddings.openai import OpenAIEmbeddings
# import pinecone 
# from langchain.vectorstores import Pinecone
# from langchain.chat_models import ChatOpenAI
# from langchain.chains.question_answering import load_qa_chain
# from datetime import datetime

# # import
# from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.vectorstores import Chroma
# import os
# from dotenv import find_dotenv, load_dotenv

# dotenv_path= find_dotenv()
# load_dotenv(dotenv_path)
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# from langchain.document_loaders import TextLoader
# from langchain.text_splitter import CharacterTextSplitter
# directory = "makroldb/marcodb/"
# # load the document and split it into chunks
# loader = DirectoryLoader(directory,glob="**/*.md", show_progress=True, use_multithreading=True)
# documents = loader.load()

# # split it into chunks
# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
# docs = text_splitter.split_documents(documents)

# # create the open-source embedding function
# embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# # load it into Chroma
# db = Chroma.from_documents(docs, embedding_function, persist_directory="./chroma_db")
# db.persist()
# # query it
# query = "events last week"
# docs = db.similarity_search(query)

# # print results
# print(docs[0].page_content)

# db3 = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)
# docs = db3.similarity_search(query)
# print(docs[0].page_content)