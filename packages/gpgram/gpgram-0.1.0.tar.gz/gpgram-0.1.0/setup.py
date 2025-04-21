from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gpgram",
    version="0.1.0",
    author="Gpgram Team",
    author_email="your.email@example.com",
    description="A modern, asynchronous Telegram Bot API library with advanced handler capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GrandpaEJ/gpgram",
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: AsyncIO",
    ],
    python_requires=">=3.8",
    install_requires=[
        "httpx>=0.23.0",
        "pydantic>=1.9.0",
        "typing-extensions>=4.0.0",
        "loguru>=0.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.18.0",
            "black>=22.1.0",
            "isort>=5.10.0",
            "mypy>=0.931",
        ],
    },
)
