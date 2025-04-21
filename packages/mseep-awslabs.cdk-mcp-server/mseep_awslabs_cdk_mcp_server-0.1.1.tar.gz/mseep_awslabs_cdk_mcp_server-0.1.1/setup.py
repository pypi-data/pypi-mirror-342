
from setuptools import setup, find_packages

setup(
    name="mseep-awslabs.cdk-mcp-server",
    version="0.1.1",
    description="An AWS CDK MCP server that provides guidance on AWS Cloud Development Kit best practices, infrastructure as code patterns, and security compliance with CDK Nag. This server offers tools to validate infrastructure designs, explain CDK Nag rules, analyze suppressions, generate Bedrock Agent schemas, and discover Solutions Constructs patterns.",
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
    install_requires=['mcp[cli]>=1.6.0', 'pydantic>=2.10.6', 'aws-lambda-powertools>=2.30.0', 'httpx>=0.27.0', 'bs4>=0.0.2'],
    keywords=["mseep"] + [],
)
