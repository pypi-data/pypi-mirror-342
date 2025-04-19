from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="bank_management_fc",
    version="0.0.1",
    author="FlowCreeper",
    author_email="caiocoutinho20120@gmail.com",
    description="A bank management package",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FlowCreeper/dio-bank-management",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.12.1',
)