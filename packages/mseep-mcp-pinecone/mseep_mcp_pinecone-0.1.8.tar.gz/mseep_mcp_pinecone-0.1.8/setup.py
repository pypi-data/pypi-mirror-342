
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-pinecone",
    version="0.1.8",
    description="Read and write to Pinecone from Claude Desktop with Model Context Protocol.",
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
    install_requires=['httpx>=0.28.0', 'jsonschema>=4.23.0', 'mcp>=1.0.0', 'pinecone>=5.4.1', 'python-dotenv>=1.0.1', 'tiktoken>=0.8.0'],
    keywords=["mseep"] + [],
)
