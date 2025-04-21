
from setuptools import setup, find_packages

setup(
    name="mseep-awslabs.cost-analysis-mcp-server",
    version="0.1.4",
    description="An AWS Labs Model Context Protocol (MCP) server for Cost Analysis of the AWS services",
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
    install_requires=['mcp[cli]>=1.6.0', 'pydantic>=2.10.6', 'boto3>=1.36.20', 'bs4>=0.0.2', 'pytest>=7.4.0', 'pytest-asyncio>=0.23.0', 'typing-extensions>=4.8.0'],
    keywords=["mseep"] + [],
)
