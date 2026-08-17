import os

from dotenv import load_dotenv

load_dotenv()

class Config:

    SECRET_KEY = os.getenv("SECRET_KEY")
    
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")

    APP_NAME = os.getenv("APP_NAME")

    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL")
    
    SENSITIVE_COLUMNS = {
    "nik",
    "no_kk",
    "no_rekening",
    "idsemesta"
}

    
    EMBEDDING_MODELS = [
        
        {
            "id": "google/gemini-embedding-2",
            "name": "Google Text Embedding 002"
        },

        {
            "id": "openai/text-embedding-3-small",
            "name": "OpenAI Text Embedding 3 Small"
        },

        {
            "id": "openai/text-embedding-3-large",
            "name": "OpenAI Text Embedding 3 Large"
        },

        
        {
            "id": "google/gemini-embedding-1",
            "name": "Google Text Embedding 001"
        },

        {
            "id": "voyage/voyage-3-large",
            "name": "Voyage 3 Large"
        },

        {
            "id": "baai/bge-large-en-v1.5",
            "name": "BAAI BGE Large"
        }

    ]
    
    LLM_MODELS = [

    {

        "id":"meta-llama/llama-3.3-70b-instruct",

        "name":"Llama 3.3 70B"

    },
    {

        "id":"meta-llama/llama-3.2-3b-instruct",

        "name":"Llama 3.2 3B"

    },
    {

        "id":"meta-llama/llama-3.2-1b-instruct",

        "name":"Llama 3.2 1B"

    },
    {

        "id":"meta-llama/llama-3.1-70b-instruct",

        "name":"Llama 3.1 70B"

    },
    {

        "id":"meta-llama/llama-3.1-8b-instruct",

        "name":"Llama 3.1 8B"

    },
    {

        "id":"google/gemini-2.5-flash-lite",

        "name":"Gemini 2.5 Flash Lite"

    }

    
    
    
    

]