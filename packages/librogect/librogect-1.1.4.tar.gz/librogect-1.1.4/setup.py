from setuptools import setup, find_packages

setup(name="librogect",  # Название вашего пакета
    version="1.1.4",  # Версия вашего пакета
    packages=find_packages(),  # Автоматически находит все пакеты
    install_requires=[],  # Зависимости вашего пакета
    description="Использование: Данная библиотека способна решать квадратные уравнения и строить графики функций. Для открытия окна с различными функциями используйте команду lib().  Прошу не брать большие отрезки осей, если у вас слабое устройство. ",
    author=" Никитос ",  # Ваше имя
    author_email="matika059@gmail.com",  # Ваш email
    classifiers=[
        "Programming Language :: Python :: 3",  # Версия Python
        "License :: OSI Approved :: MIT License",  # Лицензия
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6')