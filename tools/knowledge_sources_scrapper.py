import os
from pathlib import Path
from llama_index import  SimpleDirectoryReader

def scrape_knowledge_sources():
    # Get the current working directory
    current_dir = Path.cwd()
    
    # Construct the path to the knowledge_sources folder
    knowledge_sources_path = current_dir / "knowledge_sources"

    # Iterate through all files in the knowledge_sources folder and load only pdfs (for now)
    # Use SimpleDirectoryReader to scrape the directory
    # TODO: this could be done asynchronously to speed up the process
    required_exts = [".pdf"]

    reader = SimpleDirectoryReader(
        input_dir=str(knowledge_sources_path),
        required_exts=required_exts,
        recursive=True,
    )
    all_docs = []
    for docs in reader.iter_data():
        for doc in docs:
            # do something with the doc
            doc.text = doc.text.upper()
            all_docs.append(doc)

    print(f"Loaded {len(all_docs)} docs.")

    # Check if the folder exists
    if not knowledge_sources_path.exists():
        print(f"Error: The folder '{knowledge_sources_path}' does not exist.")
        return
    
    for document in all_docs:
        print(f"Processing file: {document.metadata['file_name']}")
        # Here you can process the content of each document
        # For demonstration, we'll just print the first 100 characters
        # (TODO: Add processing logic and handover to RAG engine)
        print(f"Content preview: {document.text[:100]}...")
        
        print("---")  # Separator between files



if __name__ == "__main__":
    scrape_knowledge_sources()