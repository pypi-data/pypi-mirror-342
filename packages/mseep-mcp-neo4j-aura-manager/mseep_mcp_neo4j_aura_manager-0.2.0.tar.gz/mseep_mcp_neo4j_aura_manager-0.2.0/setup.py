
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-neo4j-aura-manager",
    version="0.2.0",
    description="MCP Neo4j Aura Database Instance Manager",
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
    install_requires=['mcp>=1.6.0', 'requests>=2.31.0'],
    keywords=["mseep"] + [],
)
