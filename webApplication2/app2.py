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


# Чтение всех файлов в папке
def read_files_in_directory(directory_path):
    code_content = ""
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".ts") or file.endswith(".html") or file.endswith(".css"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    code_content += f"\n\n--- {file} ---\n\n"
                    code_content += f.read()
    return code_content


# Обработка загруженных файлов
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'directory' not in request.form:
        return render_template('index.html', result='Файл и директория не были загружены.', question=None)

    file = request.files['file']
    directory = request.form['directory']  # Путь к директории с кодом

    if file.filename == '':
        return render_template('index.html', result='Файл не был выбран.', question=None)

    # Сохранение файла с инструкциями
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Чтение содержимого файла с инструкциями
    with open(file_path, 'r', encoding='utf-8') as f:
        instruction_content = f.read()

    # Чтение всех файлов из указанной директории
    code_content = read_files_in_directory(directory)

    # Формирование полного промта: инструкции + код
    prompt = ChatPromptTemplate.from_template(
        "{instruction_content}\n\nAnalyze the following code and make changes as per the instructions:\n\n{code_content}")
    analysis_chain = prompt | llm | StrOutputParser()

    # Получение ответа от модели Ollama
    response = analysis_chain.invoke({"instruction_content": instruction_content, "code_content": code_content})

    # Отправка результата обратно на страницу
    return render_template('index.html', result=response, question=instruction_content)


if __name__ == '__main__':
    app.run(debug=True)
