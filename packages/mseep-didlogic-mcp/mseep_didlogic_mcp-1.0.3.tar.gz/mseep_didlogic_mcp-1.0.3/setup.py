
from setuptools import setup, find_packages

setup(
    name="mseep-didlogic_mcp",
    version="1.0.3",
    description="DIDLogic MCP server",
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
    install_requires=['annotated-types==0.7.0', 'anyio==4.9.0', 'certifi==2025.1.31', 'click==8.1.8', 'h11==0.14.0', 'httpcore==1.0.7', 'httpx==0.28.1', 'idna==3.10', 'mcp==1.4.1', 'pydantic==2.10.6', 'pydantic-core==2.27.2', 'pydantic-settings==2.8.1', 'python-dotenv==1.0.1', 'sniffio==1.3.1', 'sse-starlette==2.2.1', 'starlette==0.46.1', 'typing-extensions==4.12.2', 'uvicorn==0.34.0'],
    keywords=["mseep"] + [],
)
