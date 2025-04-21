
from setuptools import setup, find_packages

setup(
    name="mseep-awslabs.bedrock-kb-retrieval-mcp-server",
    version="0.1.3",
    description="An AWS Labs Model Context Protocol (MCP) server for Bedrock Knowledge Base Retrieval",
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
    install_requires=['boto3>=1.37.24', 'loguru>=0.7.3', 'mcp[cli]>=1.6.0', 'pydantic>=2.11.1'],
    keywords=["mseep"] + [],
)
