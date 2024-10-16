from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.memory.buffer import ConversationBufferMemory
from langchain.memory import  ConversationSummaryMemory
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser

llm = Ollama(
    model="llama3"
)

#Step 2 - here we craete a Prompt
prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            "You are a nice chatbot who explain in steps."
        ),
        HumanMessagePromptTemplate.from_template("{question}"),
    ]
)

#Step 3 - here we create a memory to remember our chat with the llm

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

summary_memory = ConversationSummaryMemory(llm=llm , memory_key="chat_history")

conversation = prompt | llm | StrOutputParser()

conversation.invoke({"question": "What is the capital of India"})

print(memory.chat_memory.messages)
print(summary_memory.chat_memory.messages)
print("Summary of the conversation is-->"+summary_memory.buffer)

#Step 7 - here we ask a another question

conversation.invoke({"question": "what is oci data science certification?"})

#Step 8 - here we print all the messagess in the memory again and see that our last question and response is printed.
print(memory.chat_memory.messages)
print(summary_memory.chat_memory.messages)
print("Summary of the conversation is-->"+summary_memory.buffer)