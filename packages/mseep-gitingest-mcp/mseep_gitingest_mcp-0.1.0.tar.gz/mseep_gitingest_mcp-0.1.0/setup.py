
from setuptools import setup, find_packages

setup(
    name="mseep-gitingest-mcp",
    version="0.1.0",
    description="Gitingest MCP server that provides Github repository info including file content, directory structure and other metadata",
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
    install_requires=['gitingest>=0.1.4', 'httpx>=0.28.1', 'mcp[cli]>=1.3.0'],
    keywords=["mseep"] + [],
)
