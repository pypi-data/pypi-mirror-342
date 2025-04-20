from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="plot-agent",
    version="0.1.0",
    author="Andre",
    author_email="andrewm4894@gmail.com",
    description="An AI-powered data visualization assistant using Plotly",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrewm4894/plot-agent",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "plotly",
        "langchain-core",
        "langchain",
        "langchain-openai",
        "pydantic",
    ],
) 