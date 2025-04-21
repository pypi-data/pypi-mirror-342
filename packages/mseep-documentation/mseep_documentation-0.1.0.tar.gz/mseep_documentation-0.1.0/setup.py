
from setuptools import setup, find_packages

setup(
    name="mseep-documentation",
    version="0.1.0",
    description="Add your description here",
    author="mseep",
    author_email="support@skydeck.ai",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=['beautifulsoup4>=4.13.3', 'httpx>=0.28.1', 'mcp[cli]>=1.3.0', 'langchain>=0.1.0', 'langchain-community>=0.1.0', 'langchain-core>=0.1.0', 'chromadb>=0.4.22'],
    keywords=["mseep"] + [],
)
