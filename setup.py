from setuptools import setup, find_packages
import sys

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dotfiles-sync",
    version="0.1.0",
    author="Your Name",
    description="A daemon app to automatically sync dotfiles with git",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "schedule>=1.1.10",
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "dotfiles-sync=dotfiles_sync.cli:main",
        ],
    },
)

