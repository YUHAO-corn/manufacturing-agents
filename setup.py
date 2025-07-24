"""
Setup script for the Manufacturing AI Agents package.
"""

from setuptools import setup, find_packages

setup(
    name="manufacturing-ai-agents",
    version="1.0.0",
    description="基于多智能体AI技术的制造业智能补货决策系统",
    author="corn",
    author_email="godcorn001@gmail.com",
    url="https://github.com/YUHAO-corn/manufacturing-ai-agents",
    packages=find_packages(),
    install_requires=[
        "langchain>=0.1.0",
        "langchain-openai>=0.0.2",
        "langchain-experimental>=0.0.40",
        "langgraph>=0.0.20",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "praw>=7.7.0",
        "stockstats>=0.5.4",
        "yfinance>=0.2.31",
        "typer>=0.9.0",
        "rich>=13.0.0",
        "questionary>=2.0.1",
        "streamlit>=1.28.0",
        "redis>=6.2.0",
        "pymongo>=4.6.0",
        "python-dotenv>=1.0.0",
    ],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "manufacturing-agents=cli.main:app",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Office/Business :: Supply Chain Management",
        "Operating System :: OS Independent",
    ],
)
