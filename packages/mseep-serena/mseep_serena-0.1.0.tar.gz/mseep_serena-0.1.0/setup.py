
from setuptools import setup, find_packages

setup(
    name="mseep-serena",
    version="0.1.0",
    description="",
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
    install_requires=['requests>=2.32.3,<3', 'pyright>=1.1.396,<2', 'overrides>=7.7.0,<8', 'python-dotenv>=1.0.0, <2', 'mcp>=1.5.0', 'fastmcp>=0.4.1', 'sensai-utils>=1.4.0', 'pydantic>=2.10.6', 'types-pyyaml>=6.0.12.20241230', 'pyyaml>=6.0.2', 'jinja2>=3.1.6', 'dotenv>=0.9.9', 'pathspec>=0.12.1', 'psutil>=7.0.0', 'agno>=1.2.15'],
    keywords=["mseep"] + [],
)
