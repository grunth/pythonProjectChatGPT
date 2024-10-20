import os
from flask import Flask, render_template, request, redirect, url_for
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
import re

# Создание экземпляра модели Ollama
llm = Ollama(model="codegemma")

app = Flask(__name__)

# Путь для загрузки файлов
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Глобальные переменные для хранения промежуточных данных
GLOBAL_RESULT = None
GLOBAL_DIRECTORY = None


# Главная страница
@app.route("/")
def index():
    return render_template("index.html", result=None, question=None)


# Чтение всех файлов в папке
def read_files_in_directory(directory_path):
    code_content = ""
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(
                (".ts", ".html", ".css")
            ):  # Указываем нужные расширения файлов
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    code_content += (
                        f"\n\n--- {file} ---\n\n"  # Добавляем имя файла для контекста
                    )
                    code_content += f.read()  # Добавляем содержимое файла
    return code_content


# Обновление файлов согласно предложенным изменениям
def apply_changes_to_files(directory, model_response):
    # Ищем все секции с изменениями в разных файлах
    pattern = r"---\s(.+?)\s---\n(.+?)(?=(---|$))"
    matches = re.findall(pattern, model_response, re.DOTALL)

    for match in matches:
        filename, changes, _ = match

        # Путь к файлу, который нужно изменить
        file_path = os.path.join(directory, filename.strip())

        # Проверяем, существует ли файл
        if os.path.exists(file_path):
            with open(file_path, "r+", encoding="utf-8") as file:
                # Читаем содержимое файла
                content = file.read()

                # Перезаписываем файл новыми изменениями
                file.seek(0)
                file.write(changes)
                file.truncate()


# Обработка загруженных файлов
@app.route("/upload", methods=["POST"])
def upload_file():
    global GLOBAL_RESULT, GLOBAL_DIRECTORY  # Используем глобальные переменные для хранения данных
    if "file" not in request.files or "directory" not in request.form:
        return render_template(
            "index.html", result="Файл и директория не были загружены.", question=None
        )

    file = request.files["file"]
    directory = request.form["directory"]

    if file.filename == "":
        return render_template(
            "index.html", result="Файл не был выбран.", question=None
        )

    # Сохранение файла с инструкциями
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Чтение содержимого файла с инструкциями
    with open(file_path, "r", encoding="utf-8") as f:
        instruction_content = f.read()

    # Чтение всех файлов из указанной директории (код)
    code_content = read_files_in_directory(directory)

    # Проверяем, что код действительно был прочитан
    if not code_content:
        return render_template(
            "index.html",
            result="Кодовые файлы в указанной директории не найдены или не удалось их прочитать.",
            question=None,
        )

    # Формирование полного промпта: инструкции + код
    prompt = ChatPromptTemplate.from_template(
        "{instruction_content}\n\nAnalyze the following code and make changes as per the instructions:\n\n{code_content}"
    )
    analysis_chain = prompt | llm | StrOutputParser()

    # Получение ответа от модели Ollama
    response = analysis_chain.invoke(
        {"instruction_content": instruction_content, "code_content": code_content}
    )

    # Сохранение результата и директории в глобальных переменных
    GLOBAL_RESULT = response
    GLOBAL_DIRECTORY = directory

    # Отправка результата на страницу без применения изменений
    return render_template(
        "index.html",
        result=response,
        question=instruction_content,
        show_apply_button=True,
    )


# Применение изменений по кнопке
@app.route("/apply-changes", methods=["POST"])
def apply_changes():
    global GLOBAL_RESULT, GLOBAL_DIRECTORY
    if GLOBAL_RESULT and GLOBAL_DIRECTORY:
        # Применение изменений к файлам
        apply_changes_to_files(GLOBAL_DIRECTORY, GLOBAL_RESULT)

        # Очистка глобальных переменных после применения изменений
        GLOBAL_RESULT = None
        GLOBAL_DIRECTORY = None

        return render_template(
            "index.html",
            result="Изменения успешно применены.",
            question=None,
            show_apply_button=False,
        )
    else:
        return render_template(
            "index.html",
            result="Нет изменений для применения.",
            question=None,
            show_apply_button=False,
        )


if __name__ == "__main__":
    app.run(debug=True)
