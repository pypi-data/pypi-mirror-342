# setup.py

from setuptools import setup, find_packages

setup(
    name="fastn-sdk",
    version="0.1.2",
    description="Python SDK for Fastn Automation Platform",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Fastn AI",
    author_email="support@fastn.ai",
    url="https://github.com/fastnai/fastn-python-sdk",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "certifi>=2020.12.5"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    keywords="fastn, automation, ai, sdk",
) 