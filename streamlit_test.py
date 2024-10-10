import streamlit as st
from langchain_community.llms import Ollama

# Инициализация модели
llm = Ollama(model="llama3")

def generate_response(input_text):
    # Генерация ответа с помощью модели
    response = llm.invoke(input_text)
    # Вывод ответа на экран
    st.info(response)

# Создание Streamlit приложения
st.title('🦜🔗 Welcome to the ChatBot')
with st.form('my_form'):
    text = st.text_area('Enter text:', 'What are the three key pieces of advice for learning how to code?')
    submitted = st.form_submit_button('Submit')
    if submitted:
        generate_response(text)

