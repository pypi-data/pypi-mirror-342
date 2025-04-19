from setuptools import setup, find_packages
import re

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("github_project_manager/_version.py", encoding="utf-8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name="github-project-manager",
    version=version,
    author="Ezra Hill",
    author_email="ezra@ezrahill.co.uk",
    description="A Python module for managing GitHub Projects (v2), issues, labels, and milestones",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ezrahill/github-project-manager",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.10",
    install_requires=[
        "requests>=2.25.0",
        "python-dotenv>=0.15.0",
    ],
)
