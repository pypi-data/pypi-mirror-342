from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="calculator-math-operations",
    version="0.0.1",
    author="LuthLucas",
    author_email="lucasmenezesfontes@gmail.com",
    description="Pacote para operações matemáticas básicas",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LuthLucas/math-operations-package.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.5',
)