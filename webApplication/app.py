import os
from flask import Flask, render_template, request
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser

# Создание экземпляра модели Ollama
llm = Ollama(model="llama3")

app = Flask(__name__)

# Путь для загрузки файлов
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Главная страница
@app.route('/')
def index():
    return render_template('index.html', result=None, question=None)


# Обработка загруженных файлов
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('index.html', result='Файл не был загружен.', question=None)

    file = request.files['file']

    if file.filename == '':
        return render_template('index.html', result='Файл не был выбран.', question=None)

    # Сохранение файла в папку uploads
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Чтение содержимого файла
    with open(file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()

    # Создание промта с использованием содержимого файла как вопроса
    prompt = ChatPromptTemplate.from_template("{file_content}")
    question_chain = prompt | llm | StrOutputParser()

    # Получение ответа от модели Ollama
    response = question_chain.invoke({"file_content": file_content})

    # Отправка результата обратно на страницу
    return render_template('index.html', result=response, question=file_content)


if __name__ == '__main__':
    app.run(debug=True)
