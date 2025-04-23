from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="fatoriais",
    version="0.0.1",
    author="Enzo Camelo",
    author_email="enzocamelo8d@gmail.com",
    description="Calcula o fatorial de um número inteiro não negativo.",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Enzo-Camelo/simple-package-template.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)