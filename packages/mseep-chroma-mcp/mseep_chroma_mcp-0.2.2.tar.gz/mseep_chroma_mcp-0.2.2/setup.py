
from setuptools import setup, find_packages

setup(
    name="mseep-chroma-mcp",
    version="0.2.2",
    description="Chroma MCP Server - Vector Database Integration for LLM Applications",
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
    install_requires=['chromadb>=1.0.3', 'cohere>=5.14.2', 'httpx>=0.28.1', 'mcp[cli]>=1.2.1', 'openai>=1.70.0', 'pillow>=11.1.0', 'pytest>=8.3.5', 'pytest-asyncio>=0.26.0', 'python-dotenv>=0.19.0', 'typing-extensions>=4.13.1', 'voyageai>=0.3.2'],
    keywords=["mseep"] + ['chroma', 'mcp', 'vector-database', 'llm', 'embeddings'],
)
