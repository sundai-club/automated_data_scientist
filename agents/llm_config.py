import os

openai_api_key = os.environ.get("OPENAI_API_KEY")

if openai_api_key:
    llm_config = {"model": "gpt-4o-mini", "api_key": os.environ.get("OPENAI_API_KEY")}
else:
    # use local LLM, install https://ollama.com/library/llama3.2:1b
    llm_config = {
        "model": "llama3.2:1b",
        "base_url": "http://127.0.0.1:11434/v1",
        "api_key": "ollama",
        "temperature": 0.5,
        "price": [
            0,
            0,
        ],
    }

print(llm_config)
