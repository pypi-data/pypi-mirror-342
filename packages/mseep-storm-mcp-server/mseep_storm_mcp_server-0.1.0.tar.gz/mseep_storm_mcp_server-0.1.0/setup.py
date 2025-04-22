
from setuptools import setup, find_packages

setup(
    name="mseep-storm-mcp-server",
    version="0.1.0",
    description="Add your description here",
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
    install_requires=['fastapi>=0.115.11', 'mcp>=1.3.0', 'requests>=2.32.3', 'uvicorn>=0.34.0'],
    keywords=["mseep"] + [],
)
