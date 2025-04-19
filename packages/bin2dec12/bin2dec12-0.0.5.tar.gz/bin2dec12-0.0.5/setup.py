from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="bin2dec12",
    version="0.0.5",
    author="GustavoGS",
    author_email="ggs.gustavo.dev@gmail.com",
    description="Convertor de números binário para decimal",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GustavoGS12/Python_Projects/tree/main/Desafios%20DIO/Bin2Dec_Package",
    packages=find_packages(),
    python_requires='>=3.0',
)