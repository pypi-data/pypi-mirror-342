from setuptools import setup, find_packages

setup(
    name="zenbroker",
    version="0.5",
    package_dir={"": "zenbroker"},
    packages=find_packages("zenbroker"),
    install_requires=[
        "pydantic>=2.0.0,<3.0.0",
        "httpx>=0.28.0,<1.0.0"
    ]
)