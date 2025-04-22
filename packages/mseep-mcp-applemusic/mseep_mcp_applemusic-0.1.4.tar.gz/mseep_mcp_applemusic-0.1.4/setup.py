
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-applemusic",
    version="0.1.4",
    description="A simple Apple Music API client for MCP",
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
    install_requires=['mcp>=1.2.1'],
    keywords=["mseep"] + [],
)
