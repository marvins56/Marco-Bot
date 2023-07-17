from langchain.document_loaders import UnstructuredFileLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.question_answering import load_qa_chain
import os
from dotenv import find_dotenv, load_dotenv
from langchain import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = OpenAI(temperature=0)


def answer_question_from_document(query: str) -> str:
    document_path="results/SqlJsonData.txt"
    # Load document
    loader = UnstructuredFileLoader(document_path)
    document = loader.load()

    # Initialize chain
    chain = load_qa_chain(llm, chain_type="refine", verbose=True, return_intermediate_steps=True)

    # Split document into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,  # Set a really small chunk size, just to show.
        chunk_overlap=0
    )
    document_chunks = text_splitter.split_documents(document)

    # Perform question answering
    result = chain({"input_documents": document_chunks[:5], "question": query}, return_only_outputs=True)

    return result['output_text']

# doc = "C:/Users/jukas/Desktop/Mackro/Marco-Bot/Marco/results/result_20230716_125005.txt"
#
# answer_question_from_document(doc, "what categories are present ")




