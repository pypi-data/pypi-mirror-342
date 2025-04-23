from setuptools import setup, find_packages

setup(
    name="ai_agent2agent",
    version="0.1.0",
    packages=find_packages(include=["agent2agent", "agent2agent.*"]),
    install_requires=[
        "pydantic>=2.0.0",
        "typing-extensions>=4.0.0",
        "starlette>=0.28.0",
        "sse-starlette>=1.0.0",
        "uvicorn>=0.22.0",
        "asyncio>=3.4.3",
    ],
    author="Eligapris",
    author_email="",
    description="A Python library for Agent-to-Agent communication",
    keywords="agent, communication, AI",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
) 