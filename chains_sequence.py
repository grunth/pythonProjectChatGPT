from langchain.prompts import (
    ChatPromptTemplate,
)
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser

llm = Ollama(
    model="llama3"
)

# Step 1: Define the prompt for generating a joke
prompt = ChatPromptTemplate.from_template("")
joke_chain = prompt | llm | StrOutputParser()

# Step 2: Define the prompt for analyzing the joke
analysis_prompt = ChatPromptTemplate.from_template("is this a funny joke? {joke}")
analysis_chain = analysis_prompt | llm | StrOutputParser()

# Generate a joke
joke = joke_chain.invoke({"topic": "bears"})
print("Generated joke:")
print(joke)

# Analyze the joke
analysis_result = analysis_chain.invoke({"joke": joke})
print("Analysis result:")
print(analysis_result)