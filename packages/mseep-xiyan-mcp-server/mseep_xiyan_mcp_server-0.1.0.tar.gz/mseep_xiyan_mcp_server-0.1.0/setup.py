
from setuptools import setup, find_packages

setup(
    name="mseep-xiyan_mcp_server",
    version="0.1.0",
    description="A Model Context Protocol (MCP) server that using XiyanSQL with MySQL databases. This server allows AI assistants to list tables, read data, and execute natual language queries.",
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
    install_requires=['mcp>=1.0.0', 'mysql-connector-python>=9.1.0', 'llama_index', 'sqlalchemy'],
    keywords=["mseep"] + [],
)
