import os
from llama_index.core import VectorStoreIndex
from llama_index.readers.file import PDFReader
from llama_index.llms.openai import OpenAI
import requests
import json
import openai
from dotenv import load_dotenv, find_dotenv
from tools.knowledge_sources_scrapper import scrape_knowledge_sources


env_path = find_dotenv()
load_dotenv(env_path)

# Get up OpenAI API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

# URL = 'http://localhost:11434/api/generate'

# data = {
#     'model': 'llama3.1:latest',
#     'prompt': 'Hello, world!'
# }

# response = requests.post(URL, data=json.dumps(data))

# if response.status_code == 200:
#     response_text = response.text
#     data = json.loads(response_text)
#     actual_response = data['response']
#     print(actual_response)
# else:
#     print(f"Error: {response.status_code} {response.text}")

# Load PDF document (single file example)
pdf_path = 'knowledge_sources/Real_Estate.pdf' # PrinRE U.S. Sector Report_Spring 2024_WEB.pdf
reader = PDFReader()
documents = reader.load_data(file=pdf_path)

# Load all PDFs in the knowledge_sources folder
# TODO
# knowledge_sources_dir = 'knowledge_sources'
# documents = scrape_knowledge_sources(knowledge_sources_dir)

# Create index from the documents
index = VectorStoreIndex.from_documents(documents)

# Create query engine
query_engine = index.as_query_engine()

# Function to perform RAG
def rag_query(question):
    response = query_engine.query(question)
    return response.response

# Function to integrate the rag answer and ask GPT-4o
def gpt_query(question, rag_answer):
    # TODO: integrate the prompt from the agent
    tmp_prompt = f"The user asked: {question}\n\nThe RAG answer is: {rag_answer}\n\nPlease provide a detailed answer to the user's question."
    # llm = OpenAI(model="gpt-4o-mini",api_key=OPENAI_API_KEY)
    # response = llm.chat(tmp_prompt)
    return tmp_prompt # response.content

# Example usage
if __name__ == "__main__":
    questions = [
        "What influences the housing prices in the U.S.?",
        "Are there any graphs or charts in the document? If so, what do they show?"
    ]

    for question in questions:
        rag_answer = rag_query(question)
        print(f"Question: {question}")
        print(f"RAG Answer: {rag_answer}")
        # gpt_answer = gpt_query(question, rag_answer)
        # print(f"GPT Answer: {gpt_answer}\n")