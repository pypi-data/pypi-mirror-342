
from setuptools import setup, find_packages

setup(
    name="mseep-emacs-mcp-server",
    version="0.1.0",
    description="Model Context Protocol (MCP) server for Emacs",
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
    install_requires=['mcp[cli]>=1.6.0', 'smartfunc>=0.2.0'],
    keywords=["mseep"] + [],
)
