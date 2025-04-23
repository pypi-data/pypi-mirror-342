#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pypro-framework",
    version="0.1.0",
    author="PyPro Team",
    author_email="aaroh.ahirrao@dpsnashik.in",
    description="A Python framework with batteries included",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypro/pypro",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Jinja2>=3.0.0",
        "MarkupSafe>=2.0.0",
        "SQLAlchemy>=1.4.0",
        # No additional dependencies to keep the core lightweight
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.12.0",
            "black>=21.5b2",
            "isort>=5.9.1",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "pyp=pypro.cli:main",
        ],
    },
)
