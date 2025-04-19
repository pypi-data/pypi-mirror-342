from setuptools import setup, find_packages # type: ignore

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Pacote_de_Processamento_de_Imagens_com_Python_DIO",
    version="0.0.1",
    author="Matheus_de_Souza_Soares",
    author_email="desouzasoaresmatheus@gmail.com",
    description="Pacote de Processamento de Imagens com Python DIO",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FledWriter3840/Pacote-de-Processamento-de-Imagens-com-Python-DIO",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)