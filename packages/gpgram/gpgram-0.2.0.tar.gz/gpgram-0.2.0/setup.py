from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gpgram",
    version="0.2.0",
    author="Gpgram Team",
    author_email="",
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
        "aiohttp>=3.8.0",  # For webhook support
        "python-multipart>=0.0.5",  # For file uploads
    ],
    keywords=[
        "telegram", "bot", "api", "async", "asyncio", "python",
        "webhook", "conversation", "inline", "keyboard", "middleware",
    ],
    project_urls={
        "Documentation": "https://gpgram.readthedocs.io/",
        "Source": "https://github.com/GrandpaEJ/gpgram",
        "Tracker": "https://github.com/GrandpaEJ/gpgram/issues",
    },
    include_package_data=True,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.18.0",
            "black>=22.1.0",
            "isort>=5.10.0",
            "mypy>=0.931",
            "twine>=4.0.0",
            "build>=0.10.0",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.15.0",
            "sphinx-copybutton>=0.5.0",
            "sphinx-autodoc-typehints>=1.12.0",
        ],
        "webhook": [
            "aiohttp>=3.8.0",
        ],
    },
)
