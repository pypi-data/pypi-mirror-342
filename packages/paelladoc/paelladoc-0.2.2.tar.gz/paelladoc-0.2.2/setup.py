"""PAELLADOC - AI-First Development Framework
See:
https://github.com/jlcases/paelladoc
"""

from setuptools import setup, find_packages

setup(
    name="paelladoc",
    version="0.2.2",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "mcp>=0.5.0",
        "sqlmodel>=0.0.8",
        "aiosqlite>=0.19.0",
        "uvicorn[standard]>=0.24.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.0",
        "alembic>=1.13.0",
    ],
) 