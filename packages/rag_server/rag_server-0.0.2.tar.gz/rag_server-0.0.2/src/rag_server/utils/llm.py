import os

from openai import OpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings

openai_client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_URL"),
)

gemini_client = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key=os.environ.get("GEMINI_API_KEY"),
)
