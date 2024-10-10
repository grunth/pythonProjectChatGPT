import os
from dotenv import load_dotenv
from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
import openai
import time

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variables
#OPENAI_API_KEY =

if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

# Initialize the Language Models
llm = OpenAI(api_key=OPENAI_API_KEY)  # Language Model
chat_model = ChatOpenAI(api_key=OPENAI_API_KEY)  # Another LLM interface

question = "What is the meaning of life?"

def get_answer(model, query):
    while True:
        try:
            return model.predict(query).strip()
        except openai.error.RateLimitError:
            print("Rate limit exceeded. Waiting 60 seconds before retrying...")
            time.sleep(60)  # Wait for 60 seconds before retrying
        except openai.error.OpenAIError as e:
            print(f"An error occurred: {e}")
            break

# Use llm.predict to get the answer
answer_llm = get_answer(llm, question)
print(question)
print(answer_llm)

# Use chat_model.predict to get the answer
answer_chat_model = get_answer(chat_model, question)
print(question)
print(answer_chat_model)
