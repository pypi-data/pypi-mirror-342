from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="yandex-search-api",
    version="0.1.0",
    author="Vasily Isaev",
    author_email="vasyaisaev31@gmail.com",
    description="Unofficial Yandex Search API client for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Vasiliy566/yandex-search-api",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "pydantic==2.11.3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)