from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="agentfleet",
    version="0.1.4",
    author="Wei Zhou",
    description="A package for managing AI agents and chatrooms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["agentfleet"],  # Instead of find_packages()
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "langchain",
        "langchain-openai",
        "langchain-community", 
        "langchain-deepseek",
        "pydantic",
        "pyjwt"
    ],
)
