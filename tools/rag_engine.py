import os
from llama_index.core import VectorStoreIndex
from llama_index.readers.file import PDFReader
from llama_index.llms.openai import OpenAI
import requests
import json
import openai
from dotenv import load_dotenv, find_dotenv
from tools.knowledge_sources_scrapper import scrape_knowledge_sources
from exa_py import Exa


env_path = find_dotenv()
load_dotenv(env_path)

# Get up OpenAI API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY
# Get up EXA API key
EXA_API_KEY = os.getenv('EXA_API_KEY')


# Function to perform RAG
def rag_query(question, **kwargs):
    # Load all PDFs in the knowledge_sources folder
    documents = scrape_knowledge_sources(kwargs.get('knowledge_sources_dir', '../knowledge_sources'))

    # Create index from the documents
    index = VectorStoreIndex.from_documents(documents)

    # Create query engine
    query_engine = index.as_query_engine()
    response = query_engine.query(question)
    # print(response.response)
    return response.response

# Function to integrate the rag answer and ask GPT-4o
def gpt_query(planner_prompt: str, rag_answer: str):
    # TODO: integrate the prompt from the agent
    tmp_prompt = f"The user asked: {planner_prompt}\n\nThe RAG answer is: {rag_answer}\n\nPlease provide a detailed answer to the user's question."
    llm = OpenAI(model="gpt-4o-mini",api_key=OPENAI_API_KEY)
    response = llm.chat(tmp_prompt)
    return response.content

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
        # TODO
        # gpt_answer = gpt_query(question, rag_answer)
        # print(f"GPT Answer: {gpt_answer}\n")


def web_rag_query(query, **kwargs):
    exa = Exa(EXA_API_KEY)
    exa_result = exa.search_and_contents(
    query,
    type="Auto",
    use_autoprompt=True,
    num_results=10,
    text=True,
    livecrawl="always",
    highlights=kwargs.get('highlights', None),
    summary=kwargs.get('summary', None),
    category=kwargs.get('category', None),
    start_published_date=kwargs.get('start_published_date', None),
    end_published_date=kwargs.get('end_published_date', None),
    include_domains=kwargs.get('include_domains', None),
    exclude_domains=kwargs.get('exclude_domains', None),
    include_text=kwargs.get('include_text', None),
    exclude_text=kwargs.get('exclude_text', None)
    )
    extracted_content = ""
    for res in exa_result.results:
        extracted_content += "Source: " + res.url
        extracted_content += "\nTitle: " + res.title
        extracted_content += "\nText: " + res.text
        extracted_content += "\n"
    return extracted_content