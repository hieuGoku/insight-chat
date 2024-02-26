"""Common settings for RAG model"""

from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

from app.logger.logger import custom_logger

def settings():
    """Set the settings for RAG."""

    Settings.llm = OpenAI(model="gpt-3.5-turbo-1106", temperature=0.0)
    Settings.embed_model = OpenAIEmbedding(
        model="text-embedding-3-small", embed_batch_size=100
    )
    Settings.context_window = 16000
    Settings.num_output = 2048

    custom_logger.info("Settings are set")
