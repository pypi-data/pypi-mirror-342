from setuptools import setup, find_packages

setup(
    name="YeatBigTonka",  # Название библиотеки
    version="0.8.0",    # Версия библиотеки
    author="Kirill Sidorov", # Ваше имя
    author_email="grias0001@gmail.com",
    description="A simple example library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my_library",  # Ссылка на репозиторий
    packages=find_packages(),  # Автоматически находит все пакеты
    install_requires=[],       # Список зависимостей
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Минимальная версия Python
)