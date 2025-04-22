
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-server-bigquery",
    version="0.2.0",
    description="A Model Context Protocol server that provides access to BigQuery. This server enables LLMs to inspect database schemas and execute queries.",
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
    install_requires=['google-cloud-bigquery>=3.27.0', 'mcp>=1.0.0'],
    keywords=["mseep"] + [],
)
