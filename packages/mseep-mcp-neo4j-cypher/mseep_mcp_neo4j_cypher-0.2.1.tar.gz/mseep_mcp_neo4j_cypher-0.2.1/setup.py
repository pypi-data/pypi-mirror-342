
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-neo4j-cypher",
    version="0.2.1",
    description="A simple Neo4j MCP server",
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
    install_requires=['mcp[cli]>=1.6.0', 'neo4j>=5.26.0', 'pydantic>=2.10.1'],
    keywords=["mseep"] + [],
)
