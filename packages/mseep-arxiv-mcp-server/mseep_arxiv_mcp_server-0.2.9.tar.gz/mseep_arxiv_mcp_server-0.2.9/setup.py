
from setuptools import setup, find_packages

setup(
    name="mseep-arxiv-mcp-server",
    version="0.2.9",
    description="A flexible arXiv search and analysis service with MCP protocol support",
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
    install_requires=['arxiv>=2.1.0', 'httpx>=0.24.0', 'python-dateutil>=2.8.2', 'pydantic>=2.8.0', 'mcp>=1.2.0', 'pymupdf4llm>=0.0.17', 'aiohttp>=3.9.1', 'python-dotenv>=1.0.0', 'pydantic-settings>=2.1.0', 'aiofiles>=23.2.1', 'uvicorn>=0.30.0', 'sse-starlette>=1.8.2', 'anyio>=4.2.0'],
    keywords=["mseep"] + [],
)
