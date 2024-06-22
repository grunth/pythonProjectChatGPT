import streamlit as st
from langchain_community.llms import Ollama

llm = Ollama(
    model="llama3"
)

def generate_response(input_text):
  st.info(llm(input_text))

#Step 4 - here we write a quick streamlit application that accepts text input (question) and
# on clicking a 'submit button call a function that generates response

st.title('🦜🔗 Welcome to the ChatBot')
with st.form('my_form'):
  text = st.text_area('Enter text:', 'What are the three key pieces of advice for learning how to code?')
  submitted = st.form_submit_button('Submit')
  if submitted :
    generate_response(text)