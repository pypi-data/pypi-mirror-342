from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as file:
    long_description = file.read()

setup(
    name="alia-apm",
    version="0.1.8",
    description="A collection of Python scripts by me, Alia. The successor of anpm.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Alia Normal",
    author_email="dan.driscoll@aussiebb.com",

    packages=find_packages(),

    license="MIT",

    install_requires=[
        "discord > 2.0",
    ],
    python_requires=">=3.12",
)
