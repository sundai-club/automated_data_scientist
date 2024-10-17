import os
from pathlib import Path
from llama_index.core import SimpleDirectoryReader
from llama_index.readers.file import PDFReader

def scrape_knowledge_sources(knowledge_sources_dir: str = '../knowledge_sources'):
    # Iterate through all files in the knowledge_sources folder and load only pdfs (for now)
    # Use SimpleDirectoryReader to scrape the directory
    # TODO: this could be done asynchronously to speed up the process
    required_exts = [".pdf"]

    reader = SimpleDirectoryReader(
        input_dir=knowledge_sources_dir,
        required_exts=required_exts,
        recursive=True,
    )


    all_docs = []
    for docs in reader.iter_data():
        for doc in docs:
            # do something with the doc
            doc.text = doc.text.upper()
            all_docs.append(doc)

    print(f"Loaded {len(all_docs)} pages.")

    # Check if the folder exists
    if not Path(knowledge_sources_dir).exists():
        print(f"current working directory: {Path.cwd()}")
        print(f"Error: The folder '{knowledge_sources_dir}' does not exist.")
        return
    
    # for document in all_docs:
    #     print(f"Processing file: {document.metadata['file_name']}")
        # Here you can process the content of each document
        # For demonstration, we'll just print the first 100 characters
        # (TODO: Add processing logic and handover to RAG engine return the processed docs)
        # print(f"Content preview: {document.text[:100]}...")
        
        # print("---")  # Separator between files
    # print(all_docs)

    return all_docs

# TODO: create a web scrapper to either: 1)download the pdfs from the web and store them in the knowledge_sources folder
# 2) scrape the text from the web pages and store them in the knowledge_sources folder

if __name__ == "__main__":
    # TODO: Write test for this function
    pass