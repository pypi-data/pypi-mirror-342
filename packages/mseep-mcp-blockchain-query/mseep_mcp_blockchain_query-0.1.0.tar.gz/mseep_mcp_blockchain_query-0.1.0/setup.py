
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-blockchain-query",
    version="0.1.0",
    description="MCP server for querying the Bitcoin blockchain",
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
    install_requires=['anyio>=4.5.0', 'black>=23.3.0', 'mcp>=1.3.0', 'httpx>=0.24.0', 'click>=8.1.7', 'pytest>=7.0.0', 'pytest-asyncio>=0.21.0', 'starlette>=0.37.2', 'uvicorn>=0.29.0'],
    keywords=["mseep"] + [],
)
