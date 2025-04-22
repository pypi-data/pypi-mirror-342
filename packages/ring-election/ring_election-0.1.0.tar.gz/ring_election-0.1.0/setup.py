# setup.py
from setuptools import setup, find_packages

setup(
    name="ring-election",                      # your package name
    version="0.1.0",                           # start with initial version
    packages=find_packages(),
    install_requires=[],                       # No external packages needed
    author="Your Name",
    author_email="your.email@example.com",
    description="Chang and Roberts ring-based leader election algorithm",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ring-election",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Or any license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
