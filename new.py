from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

llm = Ollama(
    model="llama3"
)  # assuming you have Ollama installed and have llama3 model pulled with `ollama pull llama3 `

prompt = PromptTemplate(
    input_variables=['country'],
    template="What are 5 best vacation destinations in {country}?"
)


print(prompt.format(country="Japan"))

print(llm.invoke(prompt.format(country="Japan")))

# query = "What is man?"
#
#
# response = llm.invoke(query)
#
# print(response)

# for chunks in llm.stream(query):
#     print(chunks)