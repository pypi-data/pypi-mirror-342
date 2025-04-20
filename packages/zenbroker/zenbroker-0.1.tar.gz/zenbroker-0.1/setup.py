from setuptools import setup, find_packages

setup(
    name="zenbroker",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.0.0,<3.0.0",
        "httpx>=0.28.0,<1.0.0"
    ]
)