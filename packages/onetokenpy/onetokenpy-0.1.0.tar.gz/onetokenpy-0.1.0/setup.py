from setuptools import setup, find_packages

setup(
    name="onetokenpy",
    version="0.1.0",
    description="A library for running local LLM classification tasks on data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Maxime Rivest",
    author_email="mrive052@gmail.com",
    url="https://github.com/maximerivest/onetokenpy",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0",
        "huggingface-hub>=0.17.0",
        "llama-cpp-python>=0.2.0",
    ],
    extras_require={
        "gpu": ["vllm>=0.8.4"],
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "isort>=5.0.0",
            "flake8>=5.0.0",
        ],
        "test": ["pytest>=7.0.0"],
    },
    python_requires=">=3.8",
) 