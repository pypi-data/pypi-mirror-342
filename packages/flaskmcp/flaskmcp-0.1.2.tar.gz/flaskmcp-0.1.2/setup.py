from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="flaskmcp",
    version="0.1.0",
    author="Prashant Verma",
    author_email="prashant27050@gmail.com",
    description="A Flask-based implementation of the Model Context Protocol (MCP)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vprashant/flaskmcp",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Flask",
    ],
    python_requires=">=3.7",
    install_requires=[
        "Flask>=2.0.0",
        "jsonschema>=4.0.0",
        "werkzeug>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-flask>=1.2.0",
            "black>=23.0.0",
            "isort>=5.10.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "flaskmcp=flaskmcp.cli:main",
        ],
    },
)