
from setuptools import setup, find_packages

setup(
    name="mseep-prefect-mcp-server",
    version="1.1.2",
    description="MCP server for interacting with the Prefect API",
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
    install_requires=['mcp[cli]', 'httpx>=0.24.0', 'prefect>=3.0.0'],
    keywords=["mseep"] + [],
)
