#!/usr/bin/env python3
"""
Setup script for mcp-youtube-search.
"""

import os
from setuptools import setup, find_packages

# Get version from package
with open(os.path.join("mcp_youtube_search", "__init__.py"), "r") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.strip().split("=")[1].strip(" '\"")
            break
    else:
        version = "0.1.0"

# Get long description from README
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="mcp-youtube-search",
    version=version,
    description="YouTube search MCP server and client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Arjun Prabhulal",
    author_email="code.aicloudlab@gmail.com",
    url="https://github.com/arjunprabhulal/mcp-youtube-search",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "google-adk>=0.1.0",
        "mcp>=0.1.0",
        "serpapi>=0.1.0",
        "python-dotenv>=0.19.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.11",
    keywords="mcp, youtube, search, api, serpapi",
) 