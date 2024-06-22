from langchain.prompts import (
    ChatPromptTemplate,
)
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser

llm = Ollama(
    model="llama3"
)

prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")

chain = prompt | llm | StrOutputParser()

analysis_prompt = ChatPromptTemplate.from_template("is this a funny joke? {joke}")

composed_chain = {"joke": chain} | analysis_prompt | llm | StrOutputParser()

# Invoke the composed chain and print the result
result = composed_chain.invoke({"topic": "bears"})
print("Response from LangChain:")
print(result)