from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

setup(
    name="cpf_playground",
    version="0.0.1",
    author="bernard_clint",
    author_email="bclintwood@gmail.com",
    description="A Brazilian CPF manipulator package",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bernard-rodrigues/cpf_playground/",
    packages=find_packages(),
    python_requires=">=3.5"
)