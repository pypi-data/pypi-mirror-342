from setuptools import setup, find_packages

setup(
    name="mcp-think",
    version="0.1.1",
    description="An MCP server implementing the think tool for Claude and other LLMs",
    author="Don Kang",
    author_email="donkang34@gmail.com",
    url="https://github.com/ddkang1/mcp-think",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "mcp>=1.2.0",
        "uvicorn>=0.15.0",
        "starlette>=0.17.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.18.0",
            "black>=22.1.0",
            "isort>=5.10.1",
            "mypy>=0.931",
            "flake8>=4.0.1",
        ],
    },
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "mcp-think=mcp_think.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
)