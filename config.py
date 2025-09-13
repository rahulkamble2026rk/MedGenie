import os

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your-default-api-key-here")  # Ensure this is set correctly
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "your-youtube-api-key-here")
    MODEL_NAME = "llama-3.3-70b-versatile"
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    DATA_PATH = "data/ai-medical-chatbot.csv"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200