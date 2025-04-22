
from setuptools import setup, find_packages

setup(
    name="mseep-kagimcp",
    version="0.1.3",
    description="Kagi MCP server",
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
    install_requires=['kagiapi~=0.2.1', 'mcp[cli]~=1.6.0', 'pydantic~=2.10.3'],
    keywords=["mseep"] + [],
)
